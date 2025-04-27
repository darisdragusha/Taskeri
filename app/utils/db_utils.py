from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from fastapi import Request
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv(dotenv_path=".env")

# Database URL
DB_URL = f"mysql+mysqlconnector://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"

# Create the database engine
engine = create_engine(DB_URL, echo=True, pool_pre_ping=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

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