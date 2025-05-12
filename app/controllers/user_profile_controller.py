from sqlalchemy.orm import Session
from repositories import UserProfileRepository
from models.dtos import UserProfileCreate, UserProfileUpdate
from models.user_profile import UserProfile
from typing import Optional

class UserProfileController:
    """
    Business logic for user profiles.
    """
    def __init__(self, db: Session):
        self.repo = UserProfileRepository(db)

    def create_profile(self, data: UserProfileCreate) -> UserProfile:
        return self.repo.create(data)

    def get_profile_by_user_id(self, user_id: int) -> Optional[UserProfile]:
        return self.repo.get_by_user_id(user_id)

    def update_profile(self, user_id: int, data: UserProfileUpdate) -> Optional[UserProfile]:
        return self.repo.update(user_id, data)

    def delete_profile(self, user_id: int) -> bool:
        return self.repo.delete(user_id)