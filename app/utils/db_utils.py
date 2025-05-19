from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import Request
from app.utils.env_utils import EnvironmentVariable, get_env
from contextlib import contextmanager
import os

# Database URL
DB_URL = (
    f"mysql+mysqlconnector://{get_env(EnvironmentVariable.DB_USERNAME)}:"
    f"{get_env(EnvironmentVariable.DB_PASSWORD)}@"
    f"{get_env(EnvironmentVariable.DB_HOST)}:"
    f"{get_env(EnvironmentVariable.DB_PORT)}/"
    f"{get_env(EnvironmentVariable.DB_NAME)}"
)

# Create the database engine
engine = create_engine(DB_URL, echo=True, pool_pre_ping=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_tenant_scoped_session(database_name: str) -> Session:
    tenant_db_url = f"mysql+mysqlconnector://{get_env(EnvironmentVariable.DB_USERNAME)}:{get_env(EnvironmentVariable.DB_PASSWORD)}@{get_env(EnvironmentVariable.DB_HOST)}:{get_env(EnvironmentVariable.DB_PORT)}/{database_name}"
    tenant_engine = create_engine(tenant_db_url, echo=True, pool_pre_ping=True)
    TenantSessionLocal = sessionmaker(bind=tenant_engine)
    return TenantSessionLocal()

#dependancy function for db session
async def get_db(request: Request) -> Session:
    """
    Dependency that provides the database session for the current request.

    - If a tenant-specific session exists (set by MultiTenantMiddleware), it uses it.
    - Otherwise, it creates a new session (for public routes like login/register).

    Args:
        request (Request): The FastAPI request object.

    Returns:
        Session: The SQLAlchemy session.
    """
    db = getattr(request.state, "db", None)

    if db is None:
        # No session set by middleware → create a normal session
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        # Session already created by middleware → use it
        yield db

GLOBAL_DB_URL = f"mysql+mysqlconnector://{get_env(EnvironmentVariable.DB_USERNAME)}:{get_env(EnvironmentVariable.DB_PASSWORD)}@{get_env(EnvironmentVariable.DB_HOST)}/{get_env(EnvironmentVariable.DB_NAME)}"

global_engine = create_engine(GLOBAL_DB_URL, echo=True, pool_pre_ping=True)
GlobalSessionLocal = sessionmaker(bind=global_engine, autocommit=False, autoflush=False)

@contextmanager
def get_global_db():
    db = GlobalSessionLocal()
    try:
        yield db
    finally:
        db.close()