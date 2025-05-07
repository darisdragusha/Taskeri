
from sqlalchemy.orm import Session
from typing import Optional
from models.user import User
from utils import hash_password

class UserRepository:
    """Repository class for handling user-related database operations."""

    def __init__(self, db_session: Session):
        """
        Initialize the UserRepository.

        Args:
            db_session (Session): SQLAlchemy database session.
        """
        self.db_session = db_session

    def create_user(self, email: str, password: str, first_name: str, last_name: str, department_id: Optional[int], team_id: Optional[int]) -> User:
        """
        Create a new user.

        Args:
            email (str): User's email.
            password (str): User's password (plaintext).
            first_name (str): User's first name.
            last_name (str): User's last name.
            department_id (Optional[int]): Associated department ID.
            team_id (Optional[int]): Associated team ID.

        Returns:
            User: The newly created user object.
        """
        hashed_password = hash_password(password)
        user = User(
            email=email,
            password_hash=hashed_password,
            first_name=first_name,
            last_name=last_name,
            department_id=department_id,
            team_id=team_id
        )
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by ID.

        Args:
            user_id (int): User ID.

        Returns:
            Optional[User]: User object if found, otherwise None.
        """
        return self.db_session.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by email.

        Args:
            email (str): User email.

        Returns:
            Optional[User]: User object if found, otherwise None.
        """
        return self.db_session.query(User).filter(User.email == email).first()

    def update_user(self, user_id: int, first_name: Optional[str] = None, last_name: Optional[str] = None, department_id: Optional[int] = None, team_id: Optional[int] = None) -> Optional[User]:
        """
        Update an existing user's details.

        Args:
            user_id (int): ID of the user to update.
            first_name (Optional[str]): New first name.
            last_name (Optional[str]): New last name.
            department_id (Optional[int]): New department ID.
            team_id (Optional[int]): New team ID.

        Returns:
            Optional[User]: Updated user object if found, otherwise None.
        """
        user = self.get_user_by_id(user_id)
        if user:
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if department_id:
                user.department_id = department_id
            if team_id:
                user.team_id = team_id
            self.db_session.commit()
            self.db_session.refresh(user)
            return user
        return None

    def delete_user(self, user_id: int) -> Optional[User]:
        """
        Delete a user by ID.

        Args:
            user_id (int): ID of the user to delete.

        Returns:
            Optional[User]: Deleted user object if found, otherwise None.
        """
        user = self.get_user_by_id(user_id)
        if user:
            self.db_session.delete(user)
            self.db_session.commit()
            return user
        return None
