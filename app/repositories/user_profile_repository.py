from sqlalchemy.orm import Session
from app.models.user_profile import UserProfile
from app.models.dtos.user_profile_dtos import UserProfileCreate, UserProfileUpdate
from typing import Optional

class UserProfileRepository:
    """
    Repository for managing database operations related to user profiles.
    """

    def __init__(self, db: Session):
        """
        Initialize the repository with a database session.
        """
        self.db = db

    def create(self, data: UserProfileCreate) -> UserProfile:
        """
        Create a new user profile in the database.
        """
        profile = UserProfile(**data.model_dump())
        self.db.add(profile)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def get_by_user_id(self, user_id: int) -> Optional[UserProfile]:
        """
        Retrieve a user profile by the user ID.
        """
        return self.db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

    def update(self, user_id: int, data: UserProfileUpdate) -> Optional[UserProfile]:
        """
        Update an existing user profile.
        """
        profile = self.get_by_user_id(user_id)
        if not profile:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(profile, key, value)
        self.db.commit()
        self.db.refresh(profile)
        return profile

    def delete(self, user_id: int) -> bool:
        """
        Delete a user profile by user ID.
        """
        profile = self.get_by_user_id(user_id)
        if not profile:
            return False
        self.db.delete(profile)
        self.db.commit()
        return True