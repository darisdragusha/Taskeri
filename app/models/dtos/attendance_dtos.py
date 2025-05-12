from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AttendanceResponse(BaseModel):
    id: int
    user_id: int
    check_in: datetime
    check_out: Optional[datetime]

    class Config:
        orm_mode = True
