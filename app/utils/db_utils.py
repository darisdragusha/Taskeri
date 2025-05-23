from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import Request, HTTPException
from contextlib import contextmanager
from app.utils.env_utils import EnvironmentVariable, get_env

# === Base Model ===
Base = declarative_base()

# === GLOBAL DB URL ===
GLOBAL_DB_URL = (
    f"mysql+mysqlconnector://{get_env(EnvironmentVariable.DB_USERNAME)}:"
    f"{get_env(EnvironmentVariable.DB_PASSWORD)}@"
    f"{get_env(EnvironmentVariable.DB_HOST)}:"
    f"{get_env(EnvironmentVariable.DB_PORT)}/"
    f"{get_env(EnvironmentVariable.DB_NAME)}"
)

# === GLOBAL ENGINE & SESSION ===
global_engine = create_engine(GLOBAL_DB_URL, echo=True, pool_pre_ping=True)
GlobalSessionLocal = sessionmaker(bind=global_engine, autocommit=False, autoflush=False)

@contextmanager
def get_global_db():
    """
    Context manager to get a database session for the global (non-tenant) schema.

    Yields:
        Session: SQLAlchemy database session for the global schema.
    Ensures:
        The session is properly closed after use.
    """
    db = GlobalSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_tenant_session(schema_name: str) -> Session:
    """
    Create a new SQLAlchemy session connected to a specific tenant schema.

    Args:
        schema_name (str): The name of the tenant's MySQL schema.

    Returns:
        Session: SQLAlchemy database session scoped to the tenant schema.
    """
    tenant_db_url = (
        f"mysql+mysqlconnector://{get_env(EnvironmentVariable.DB_USERNAME)}:"
        f"{get_env(EnvironmentVariable.DB_PASSWORD)}@"
        f"{get_env(EnvironmentVariable.DB_HOST)}:"
        f"{get_env(EnvironmentVariable.DB_PORT)}/"
        f"{schema_name}"
    )
    tenant_engine = create_engine(tenant_db_url, echo=True, pool_pre_ping=True)
    TenantSessionLocal = sessionmaker(bind=tenant_engine, autocommit=False, autoflush=False)
    return TenantSessionLocal()

async def get_db(request: Request) -> Session:
    """
    FastAPI dependency to provide a database session per request.

    If the middleware has attached a tenant-specific session to `request.state.db`,
    it uses that. Otherwise, it defaults to a global session.

    Args:
        request (Request): FastAPI request object.

    Yields:
        Session: SQLAlchemy session for the request.
    """
    db = getattr(request.state, "db", None)

    if db is None:
        db = GlobalSessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        yield db

def switch_schema(db: Session, schema_name: str):
    """
    Explicitly switches the current database session to a given MySQL schema.

    This is useful when using a shared connection pool where schema needs to be set dynamically.

    Args:
        db (Session): SQLAlchemy session.
        schema_name (str): Target schema name to switch to.

    Raises:
        HTTPException: If the schema switch fails.
    """
    try:
        db.execute(text(f"USE {schema_name};"))
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to switch schema: {str(e)}")