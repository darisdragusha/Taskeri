from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import date
from enum import Enum
from datetime import datetime



class ProjectStatusEnum(str, Enum):
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ON_HOLD = "On Hold"


class ProjectCreate(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    status: Optional[ProjectStatusEnum] = ProjectStatusEnum.NOT_STARTED

    model_config = {
        "from_attributes": True
    }


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[ProjectStatusEnum] = None

    model_config = {
        "from_attributes": True
    }


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    start_date: date
    end_date: Optional[date]
    status: ProjectStatusEnum
    created_at: Optional[datetime]

    model_config = {
        "from_attributes": True
    }


class ProjectStatistics(BaseModel):
    Not_Started: int = 0
    In_Progress: int = 0
    Completed: int = 0
    On_Hold: int = 0

    model_config = {
        "from_attributes": True
    }

    @classmethod
    def from_dict(cls, stats: Dict[str, int]) -> "ProjectStatistics":
        return cls(
            Not_Started=stats.get("Not Started", 0),
            In_Progress=stats.get("In Progress", 0),
            Completed=stats.get("Completed", 0),
            On_Hold=stats.get("On Hold", 0),
        )
