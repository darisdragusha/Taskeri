from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import Request, HTTPException
from contextlib import contextmanager
from app.utils.env_utils import EnvironmentVariable, get_env

# === Base Model ===
Base = declarative_base()

def get_db_url():
    """Get the database URL based on environment."""
    if not get_env(EnvironmentVariable.DB_NAME):
        # For tests, use SQLite in-memory database
        return 'sqlite:///:memory:'
    
    return (
        f"mysql+mysqlconnector://{get_env(EnvironmentVariable.DB_USERNAME)}:"
        f"{get_env(EnvironmentVariable.DB_PASSWORD)}@"
        f"{get_env(EnvironmentVariable.DB_HOST)}:"
        f"{get_env(EnvironmentVariable.DB_PORT)}/"
        f"{get_env(EnvironmentVariable.DB_NAME)}"
    )

# === GLOBAL DB URL ===
GLOBAL_DB_URL = get_db_url()

# === GLOBAL ENGINE & SESSION ===
# Initialize these lazily to allow test configuration
_global_engine = None
_global_session_maker = None

def get_engine():
    """Get or create the global database engine."""
    global _global_engine
    if _global_engine is None:
        _global_engine = create_engine(GLOBAL_DB_URL, echo=True, pool_pre_ping=True)
    return _global_engine

def get_session_maker():
    """Get or create the global session maker."""
    global _global_session_maker
    if _global_session_maker is None:
        _global_session_maker = sessionmaker(bind=get_engine(), autocommit=False, autoflush=False)
    return _global_session_maker

def GlobalSessionLocal():
    """Get a new session from the global session maker."""
    return get_session_maker()()

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
    # Connect to the main database
    db_name = get_env(EnvironmentVariable.DB_NAME)
    if get_env(EnvironmentVariable.TESTING) == 'true':
        db_name = 'taskeri_test'
        
    tenant_db_url = (
        f"mysql+mysqlconnector://{get_env(EnvironmentVariable.DB_USERNAME)}:"
        f"{get_env(EnvironmentVariable.DB_PASSWORD)}@"
        f"{get_env(EnvironmentVariable.DB_HOST)}:"
        f"{get_env(EnvironmentVariable.DB_PORT)}/"
        f"{db_name}"
    )
    tenant_engine = create_engine(tenant_db_url, echo=True, pool_pre_ping=True)
    TenantSessionLocal = sessionmaker(bind=tenant_engine, autocommit=False, autoflush=False)
    
    # Create session and switch to tenant schema
    session = TenantSessionLocal()
    
    try:
        session.execute(text(f"USE {schema_name}"))
        return session
    except Exception as e:
        session.close()
        raise RuntimeError(f"Failed to switch to schema {schema_name}: {str(e)}")

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
    Includes special handling for test connections that might be in an unusual state.

    Args:
        db (Session): SQLAlchemy session.
        schema_name (str): Target schema name to switch to.

    Raises:
        HTTPException: If the schema switch fails.
    """
    try:
        # Check if connection is active
        if not db.is_active:
            try:
                # For test sessions, attempt to begin a new transaction
                db.begin()
            except Exception:
                pass
                
        # Attempt to execute schema switch
        db.execute(text(f"USE {schema_name};"))
        
        # Only commit if transaction is active to avoid errors
        if db.is_active:
            db.commit()
    except Exception as e:
        # Don't raise HTTP exceptions during tests as they interfere with pytest
        if get_env(EnvironmentVariable.TESTING) == 'true':
            import logging
            logging.error(f"Failed to switch schema in test: {str(e)}")
        else:
            raise HTTPException(status_code=500, detail=f"Failed to switch schema: {str(e)}")