from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    message: str
    read_status: bool
    created_at: datetime

    class Config:
        orm_mode = True

class NotificationCreate(BaseModel):
    user_id: int
    message: str
    read_status: Optional[bool] = False  # default unread when creating notification
