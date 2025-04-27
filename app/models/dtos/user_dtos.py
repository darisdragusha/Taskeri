# app/schemas/user_schema.py
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: str
    first_name: str
    last_name: str
    department_id: Optional[int] = None
    team_id: Optional[int] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    department_id: Optional[int] = None
    team_id: Optional[int] = None

class UserResponse(UserBase):
    id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True
        from_attributes = True  
    
    @validator('created_at', 'updated_at', pre=True)
    def datetime_to_str(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()  # Converts datetime to ISO 8601 string
        return v
