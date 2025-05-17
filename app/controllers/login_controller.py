from app.repositories import TenantUserRepository, UserRepository
from auth.auth import auth_service
from app.utils import hash_password, verify_password
from sqlalchemy.orm import Session
from sqlalchemy import text
import re
from app.utils.env_utils import EnvironmentVariable, get_env

class LoginController:
    """
    Controller class that contains the business logic for user authentication.

    This class interacts with the repository layer to verify user credentials and
    generate a JWT token. It is responsible for handling the business logic between
    the view and the database.
    """
    def __init__(self, db: Session):
        """
        Initializes the LoginController with the database session.

        Args:
            db (Session): The database session to interact with the database.
        """
        self.db = db
        

    async def authenticate_user(self, email: str, password: str):
        """
        Authenticates the user by verifying their credentials against the database.

        This method checks the provided email and password. If the credentials are valid,
        a JWT token is generated for the user. If the credentials are invalid, None is returned.

        Args:
            email (str): The email provided by the user during login.
            password (str): The password provided by the user during login.

        Returns:
            str | None: Returns the JWT access token if authentication is successful, otherwise None.
        """
        # Validate the input parameters
        if not email or not password:
            return None
        
        global_db = get_env(EnvironmentVariable.DB_NAME, "taskeri_global")
        self.db.execute(text(f"USE {global_db}"))
    
        self.db.commit()
        tenant_user_repo = TenantUserRepository(self.db)
        
        # Get tenant user by email
        tenant_user = tenant_user_repo.get_by_email(email)
        schema = tenant_user.tenant_schema
        tenant_id = tenant_user.id

        # Validate the schema name to prevent SQL injection
        if not re.match(r"^[a-zA-Z0-9_]+$", schema):
            raise ValueError("Invalid tenant schema name")
            
        # Switch to the tenant schema
        self.db.execute(text(f"USE tenant_{schema}"))
        self.db.commit()

        # Re-initialize repo AFTER switching schema
        user_repo = UserRepository(self.db)

        # Get the user by email and verify the password
        user = user_repo.get_user_by_email(email)
        valid_user = (user and user.email == email and verify_password(password, user.password_hash))

        # If user is valid, generate and return the JWT token
        if valid_user:
            access_token = auth_service.create_access_token(user_id=user.id,tenant_id=tenant_id, tenant_name=schema)
            return access_token
        
        # If authentication fails, return None
        return None
