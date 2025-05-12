from sqlalchemy.orm import Session
from models.user_profile import UserProfile
from models.dtos import UserProfileCreate, UserProfileUpdate
from typing import Optional

class UserProfileRepository:
    """
    Repository for managing user profiles.
    """
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: UserProfileCreate) -> UserProfile:
        profile = UserProfile(**data.model_dump())
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def get_by_user_id(self, user_id: int) -> Optional[UserProfile]:
        return self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    def update(self, user_id: int, data: UserProfileUpdate) -> Optional[UserProfile]:
        profile = self.get_by_user_id(user_id)
        if not profile:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(profile, key, value)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def delete(self, user_id: int) -> bool:
        profile = self.get_by_user_id(user_id)
        if not profile:
            return False
        self.db.delete(profile)
        self.db.commit()
        return True