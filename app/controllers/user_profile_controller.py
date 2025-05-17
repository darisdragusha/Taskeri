from sqlalchemy.orm import Session
from typing import Optional
from app.repositories.user_profile_repository import UserProfileRepository
from app.models.dtos.user_profile_dtos import UserProfileCreate, UserProfileUpdate
from app.models.user_profile import UserProfile

class UserProfileController:
    """
    Controller for handling business logic related to user profiles.
    """

    def __init__(self, db: Session):
        """
        Initialize the controller with a database session.
        """
        self.repo = UserProfileRepository(db)

    def create_profile(self, data: UserProfileCreate) -> UserProfile:
        """
        Handle creation of a new user profile.
        """
        return self.repo.create(data)

    def get_profile_by_user_id(self, user_id: int) -> Optional[UserProfile]:
        """
        Retrieve a user profile by user ID.
        """
        return self.repo.get_by_user_id(user_id)

    def update_profile(self, user_id: int, data: UserProfileUpdate) -> Optional[UserProfile]:
        """
        Update an existing user profile.
        """
        return self.repo.update(user_id, data)

    def delete_profile(self, user_id: int) -> bool:
        """
        Delete a user profile.
        """
        return self.repo.delete(user_id)