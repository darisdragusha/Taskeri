from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from repositories.user_repository import UserRepository
from utils.db_utils import get_db
from models.dtos import UserCreate, UserUpdate, UserResponse

class UserController:
    """Controller class for handling user operations."""

    def __init__(self, db_session: Session = Depends(get_db)):
        """
        Initialize the UserController.

        Args:
            db_session (Session): SQLAlchemy database session.
        """
        self.repository = UserRepository(db_session)

    def create_user(self, user_create: UserCreate) -> UserResponse:
        """
        Create a new user.

        Args:
            user_create (UserCreate): Data for the new user.

        Returns:
            UserResponse: Created user response.
        """
        user = self.repository.create_user(
            email=user_create.email,
            password=user_create.password,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            department_id=user_create.department_id,
            team_id=user_create.team_id
        )
        return UserResponse.from_orm(user)

    def get_user(self, user_id: int) -> UserResponse:
        """
        Get a user by ID.

        Args:
            user_id (int): User ID.

        Returns:
            UserResponse: Retrieved user response.
        """
        user = self.repository.get_user_by_id(user_id)
        if user:
            return UserResponse.from_orm(user)
        raise HTTPException(status_code=404, detail="User not found")

    def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        """
        Update a user's information.

        Args:
            user_id (int): User ID.
            user_update (UserUpdate): Updated user data.

        Returns:
            UserResponse: Updated user response.
        """
        user = self.repository.update_user(
            user_id,
            first_name=user_update.first_name,
            last_name=user_update.last_name,
            department_id=user_update.department_id,
            team_id=user_update.team_id
        )
        if user:
            return UserResponse.from_orm(user)
        raise HTTPException(status_code=404, detail="User not found")

    def delete_user(self, user_id: int) -> dict:
        """
        Delete a user.

        Args:
            user_id (int): User ID.

        Returns:
            dict: Success message.
        """
        user = self.repository.delete_user(user_id)
        if user:
            return {"message": "User deleted successfully"}
        raise HTTPException(status_code=404, detail="User not found")
