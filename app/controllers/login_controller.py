from repositories.login_repository import LoginRepository
from auth.auth import auth_service
from utils.auth_utils import hash_password, verify_password
from sqlalchemy.orm import Session

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
        self.login_repo = LoginRepository(db)

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
        
        #Hash the password using bcrypt
        hashed_password = hash_password(password)

        # Verify user credentials through the repository layer
        user = self.login_repo.verify_user_credentials(email, hashed_password)
        
        valid_user = (user and user.email == email and verify_password(hashed_password, user.password))
        # If user is valid, generate and return the JWT token
        if valid_user:
            access_token = auth_service.create_access_token(data={"sub": user.id, "tenant_id": user.tenant_id})
            return access_token
        
        # If authentication fails, return None
        return None
