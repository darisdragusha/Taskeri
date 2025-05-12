from pydantic import BaseModel
from typing import Optional

class UserProfileCreate(BaseModel):
    user_id: int
    position: Optional[str] = None
    skills: Optional[str] = None
    bio: Optional[str] = None
    profile_pic: Optional[str] = None

class UserProfileUpdate(BaseModel):
    position: Optional[str] = None
    skills: Optional[str] = None
    bio: Optional[str] = None
    profile_pic: Optional[str] = None

class UserProfileResponse(BaseModel):
    user_id: int
    position: Optional[str]
    skills: Optional[str]
    bio: Optional[str]
    profile_pic: Optional[str]

    class Config:
        orm_mode = True