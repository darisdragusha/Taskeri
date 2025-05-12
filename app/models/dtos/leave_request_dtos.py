from datetime import date
from pydantic import BaseModel, Field
from typing import Literal


class LeaveRequestCreate(BaseModel):
    leave_type: Literal["Vacation", "Sick Leave", "Personal", "Other"] = Field(..., description="Type of leave")
    start_date: date = Field(..., description="Start date of the leave")
    end_date: date = Field(..., description="End date of the leave")


class LeaveRequestResponse(BaseModel):
    id: int
    user_id: int
    leave_type: Literal["Vacation", "Sick Leave", "Personal", "Other"]
    start_date: date
    end_date: date
    status: Literal["Pending", "Approved", "Rejected"]

    class Config:
        orm_mode = True
