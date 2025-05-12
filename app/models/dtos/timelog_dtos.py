from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class TimeLogCreate(BaseModel):
    user_id: int
    task_id: int
    start_time: datetime
    end_time: datetime

class TimeLogUpdate(BaseModel):
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[int] = None
