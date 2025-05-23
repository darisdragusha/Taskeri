import os
import pytest
import sqlalchemy as sa
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import sessionmaker, Session
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.utils.env_utils import EnvironmentVariable, get_env
from app.utils.db_utils import Base, get_session_maker, switch_schema
from fastapi.testclient import TestClient
from fastapi import Request
from app.app import app
import importlib
import glob
from pathlib import Path

def import_all_models():
    """Import all model files to ensure they're registered with SQLAlchemy"""
    models_dir = Path(__file__).parent.parent / "app" / "models"
    for file_path in glob.glob(str(models_dir / "*.py")):
        if not file_path.endswith("__init__.py"):
            module_name = f"app.models.{Path(file_path).stem}"
            importlib.import_module(module_name)

@pytest.fixture(scope='session', autouse=True)
def setup_test_env():
    """Set up test environment variables."""
    # Store original env vars
    original_env = {
        'TESTING': os.environ.get('TESTING'),
        'DB_NAME': os.environ.get('DB_NAME'),
        'SECRET_KEY': os.environ.get('SECRET_KEY', 'test_secret'),
        'ALGORITHM': os.environ.get('ALGORITHM', 'HS256'),
        'ACCESS_TOKEN_EXPIRE_MINUTES': os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', '30')
    }
    
    # Set test env vars for MySQL
    os.environ['TESTING'] = 'true'
    os.environ['DB_NAME'] = 'taskeri_test'
    os.environ['DB_HOST'] = 'localhost'
    os.environ['DB_PORT'] = '3306'
    os.environ['DB_USERNAME'] = 'root'
    os.environ['DB_PASSWORD'] = '0209'
    os.environ['SECRET_KEY'] = 'test_secret'
    os.environ['ALGORITHM'] = 'HS256'
    os.environ['ACCESS_TOKEN_EXPIRE_MINUTES'] = '30'
    
    yield
    
    # Restore original env vars
    for key, value in original_env.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value

@pytest.fixture(scope='session')
def engine():
    """Create a MySQL database engine for testing."""
    from app.utils.db_utils import get_db_url
    import_all_models()
    
    # Create initial connection to MySQL root
    root_url = (
        f"mysql+mysqlconnector://{os.environ['DB_USERNAME']}:"
        f"{os.environ['DB_PASSWORD']}@"
        f"{os.environ['DB_HOST']}:"
        f"{os.environ['DB_PORT']}"
    )
    root_engine = create_engine(root_url)
    
    with root_engine.connect() as conn:
        # Drop databases if they exist
        conn.execute(text('DROP DATABASE IF EXISTS taskeri_test'))
        conn.execute(text('DROP DATABASE IF EXISTS taskeri_global'))
        conn.execute(text('DROP DATABASE IF EXISTS tenant_test_tenant'))
        conn.commit()
        
        # Create test databases
        conn.execute(text('CREATE DATABASE taskeri_test'))
        conn.execute(text('CREATE DATABASE taskeri_global'))
        conn.execute(text('CREATE DATABASE tenant_test_tenant'))
        conn.commit()
    
    # Create test engine with taskeri_test database
    test_engine = create_engine(
        root_url + '/taskeri_test',
        echo=True,
        pool_pre_ping=True
    )
    
    # Create tables
    with test_engine.connect() as conn:
        # Create tables in global schema
        conn.execute(text('USE taskeri_global'))
        tables_global = [table for table in Base.metadata.sorted_tables if not table.schema or table.schema == 'taskeri_global']
        for table in tables_global:
            table.schema = 'taskeri_global'
        Base.metadata.create_all(bind=conn, tables=tables_global)
        
        # Create tables in tenant schema
        conn.execute(text('USE tenant_test_tenant'))
        tables_tenant = [table for table in Base.metadata.sorted_tables if table.schema != 'taskeri_global']
        for table in tables_tenant:
            table.schema = 'tenant_test_tenant'
        Base.metadata.create_all(bind=conn, tables=tables_tenant)
        
        conn.commit()
    
    yield test_engine
    
    # Cleanup after all tests
    with root_engine.connect() as conn:
        conn.execute(text('DROP DATABASE IF EXISTS taskeri_test'))
        conn.execute(text('DROP DATABASE IF EXISTS taskeri_global'))
        conn.execute(text('DROP DATABASE IF EXISTS tenant_test_tenant'))
        conn.commit()

@pytest.fixture(scope='function')
def db_session(engine):
    """Create a new database session for a test."""
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    # Start with global schema
    connection.execute(text('USE taskeri_global'))
    session.execute(text('USE taskeri_global'))
    
    yield session

    try:
        # Rollback transaction and close session
        session.close()
    except Exception:
        pass
        
    try:
        transaction.rollback()
    except Exception:
        pass
        
    try:
        connection.close()
    except Exception:
        pass

@pytest.fixture
def test_db(db_session):
    """Dependency override for getting DB sessions in API tests."""
    try:
        yield db_session
    finally:
        try:
            db_session.rollback()
        except Exception:
            pass

@pytest.fixture
def client(test_db, engine):
    """Test client with database session override."""
    async def test_session_middleware(request: Request, call_next):
        try:
            # Create a new session for each request to prevent connection issues
            connection = engine.connect()
            session = sessionmaker(bind=connection)()
            
            # Make sure we're using the global schema at the start of each request
            session.execute(text('USE taskeri_global'))
            
            # Store the database session in the request state
            request.state.test_db = session
            
            # List of public routes that should be processed without token validation
            from app.config.routes_config import PUBLIC_ROUTES
            
            # For public routes, remain in global schema
            if request.url.path in PUBLIC_ROUTES:
                session.execute(text('USE taskeri_global'))
            
            # Process the request
            response = await call_next(request)
            
            # Return to global schema after processing
            try:
                session.execute(text('USE taskeri_global'))
            except Exception:
                pass
                
            # Close the session at the end of the request
            try:
                session.close()
                connection.close()
            except Exception:
                pass
                
            return response
        except Exception as e:
            # Log the exception but allow test to continue
            import logging
            logging.error(f"Error in test_session_middleware: {str(e)}")
            raise

    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.rollback()
    
    # Clear any existing middleware to prevent conflicts
    app.middleware_stack = None

    # Create a fresh FastAPI app for testing to ensure clean state
    from fastapi import FastAPI
    from app.app import setup_routes, setup_middlewares, setup_cors
    
    # Create a test-specific version of the app to prevent conflicts
    test_app = FastAPI()
    setup_routes(test_app)
    
    # Add test session middleware before the multi-tenant middleware
    test_app.middleware("http")(test_session_middleware)
    
    # Override database dependencies
    from app.utils.db_utils import get_db
    from app.middleware.multi_tenant_middleware import MultiTenantMiddleware
    test_app.dependency_overrides[get_db] = override_get_db
    test_app.dependency_overrides[get_session_maker] = override_get_db
    
    # Add the multi-tenant middleware
    test_app.add_middleware(MultiTenantMiddleware)
    
    # Apply CORS if needed
    setup_cors(test_app)
    
    with TestClient(test_app) as test_client:
        yield test_client
        
    # No need to clean up the original app since we used a separate test app

@pytest.fixture
def test_user(db_session):
    """Create a test tenant user in the database and return user info"""
    from app.models.tenant_user import TenantUser
    from app.models.user import User
    from sqlalchemy import text
    from app.utils.auth_utils import hash_password as get_password_hash
    
    # Switch to global schema and add tenant user
    db_session.execute(text('USE taskeri_global'))
    
    # Check if user already exists
    existing_user = db_session.query(TenantUser).filter_by(email="test@example.com").first()
    
    if not existing_user:
        # Create tenant user in global schema
        tenant_user = TenantUser(
            email="test@example.com",
            tenant_schema="test_tenant"
        )
        db_session.add(tenant_user)
        db_session.commit()
        tenant_id = tenant_user.id
    else:
        tenant_id = existing_user.id
    
    # Switch to tenant schema and add user
    db_session.execute(text('USE tenant_test_tenant'))
    
    # Check if user already exists in tenant schema
    existing_tenant_user = db_session.query(User).filter_by(email="test@example.com").first()
    
    if not existing_tenant_user:
        # Create user in tenant schema
        user = User(
            email="test@example.com",
            password_hash=get_password_hash("password123"),
            first_name="Test",
            last_name="User"
        )
        db_session.add(user)
        db_session.commit()
        user_id = user.id
    else:
        user_id = existing_tenant_user.id
    
    # Switch back to global schema
    db_session.execute(text('USE taskeri_global'))
    
    return {
        "id": user_id,
        "email": "test@example.com",
        "tenant_id": tenant_id,
        "tenant_name": "test_tenant"
    }

@pytest.fixture
def auth_token(test_user):
    """Generate JWT token for test authentication"""
    from app.auth.auth import auth_service
    return auth_service.create_access_token(
        user_id=test_user["id"],
        tenant_id=test_user["tenant_id"],
        tenant_name=test_user["tenant_name"]
    )

@pytest.fixture
def authorized_client(client, auth_token):
    """Return an authenticated test client"""
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {auth_token}"
    }
    return client

@pytest.fixture
def tenant_session(db_session):
    """Create a session for tenant-specific operations."""
    # Switch to tenant schema
    db_session.execute(text('USE tenant_test_tenant'))
    yield db_session
    # Switch back to global schema
    db_session.execute(text('USE taskeri_global'))

@pytest.fixture
def mock_comment_response():
    """Create a mock response for a comment"""
    from app.models.dtos.task_dtos import CommentResponse, UserBasicInfo
    from datetime import datetime
    
    user = UserBasicInfo(
        id=1,
        first_name="Test",
        last_name="User",
        email="test@example.com"
    )
    
    return CommentResponse(
        id=1,
        content="Test comment",
        user_id=1,
        task_id=1,
        created_at=datetime.utcnow().isoformat(),
        user=user
    )

@pytest.fixture
def mock_project_response():
    """Create a mock response for a project"""
    from app.models.dtos.project_dtos import ProjectResponse, ProjectStatusEnum
    from datetime import date, datetime
    
    return ProjectResponse(
        id=1,
        name="Test Project",
        description="A test project",
        start_date=date(2025, 5, 1),
        end_date=date(2025, 6, 1),
        status=ProjectStatusEnum.IN_PROGRESS,
        created_at=datetime.utcnow()
    )

@pytest.fixture
def mock_user_response():
    """Create a mock response for a user"""
    from app.models.dtos.user_dtos import UserResponse
    from datetime import datetime
    
    return UserResponse(
        id=1,
        email="test@example.com",
        first_name="Test",
        last_name="User",
        department_id=None,
        team_id=None,
        created_at=datetime.utcnow().isoformat(),
        updated_at=datetime.utcnow().isoformat(),
        role_id=None
    )
