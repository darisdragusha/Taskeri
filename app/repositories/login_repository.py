from sqlalchemy.orm import Session
from models.tenant_user import TenantUser
from passlib.context import CryptContext

class LoginRepository:
    """
    Repository class that interacts with the database for user authentication.

    This class is responsible for querying the database to verify user credentials
    and retrieving user data from the database. It abstracts away the database 
    operations for user-related actions.
    """
    def __init__(self, db: Session):
        """
        Initializes the LoginRepository with the database session.

        Args:
            db (Session): The database session to interact with the database.
        """
        self.db = db

    def verify_user_credentials(self, email: str, password: str):
        """
        Verifies the user's credentials by checking the username and password in the database.

        This method checks if the provided username exists in the database and if the
        provided password matches the stored hash using bcrypt. If the credentials are
        correct, the corresponding user object is returned; otherwise, None is returned.

        Args:
            username (str): The username to look up in the database.
            password (str): The password to verify against the stored hash.

        Returns:
            User | None: Returns the user object if credentials are valid, otherwise None.
        """
        # Query the database to find the user by username
        user = self.db.query(TenantUser).filter(TenantUser.email == email).first()

        # If user exists and the password is valid, return the user
        if user: 
            return user
        
        # If credentials are invalid, return None
        return None
