# app/schemas/user_schema.py
from pydantic import BaseModel, field_validator
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
    role_id: Optional[int] = None

class UserUpdate(UserBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    department_id: Optional[int] = None
    team_id: Optional[int] = None

class UserResponse(UserBase):
    id: int
    created_at: str
    updated_at: str
    role_id: Optional[int] = None

    model_config = {
        "from_attributes": True
    }
    
    @field_validator('created_at', 'updated_at', mode='before')
    def datetime_to_str(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()  # Converts datetime to ISO 8601 string
        return v
