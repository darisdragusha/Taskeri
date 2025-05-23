from pydantic import BaseModel, Field
from typing import Optional, Dict, List
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
    assigned_user_ids: Optional[List[int]] = None

    model_config = {
        "from_attributes": True
    }


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[ProjectStatusEnum] = None
    assigned_user_ids: Optional[List[int]] = None

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
    total_projects: int = 0
    not_started_projects: int = 0
    in_progress_projects: int = 0
    completed_projects: int = 0
    on_hold_projects: int = 0

    model_config = {
        "from_attributes": True
    }

    @classmethod
    def from_dict(cls, stats: Dict[str, int]) -> "ProjectStatistics":
        total = sum([
            stats.get("Not Started", 0),
            stats.get("In Progress", 0),
            stats.get("Completed", 0),
            stats.get("On Hold", 0)
        ])
        return cls(
            total_projects=total,
            not_started_projects=stats.get("Not Started", 0),
            in_progress_projects=stats.get("In Progress", 0),
            completed_projects=stats.get("Completed", 0),
            on_hold_projects=stats.get("On Hold", 0),
        )
