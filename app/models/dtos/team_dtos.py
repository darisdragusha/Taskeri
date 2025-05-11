from pydantic import BaseModel, Field
from typing import Optional, Dict


class TeamCreate(BaseModel):
    name: str = Field(..., max_length=100, description="Name of the team")
    department_id: int = Field(..., description="ID of the department the team belongs to")


class TeamUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100, description="Updated name of the team")
    department_id: Optional[int] = Field(None, description="Updated department ID")


class TeamResponse(BaseModel):
    id: int
    name: str
    department_id: Optional[int]

    class Config:
        from_attributes = True  


class TeamStatistics(BaseModel):
    stats: Dict[int, int]  # department_id -> number of teams

    @classmethod
    def from_dict(cls, data: Dict[int, int]) -> "TeamStatistics":
        return cls(stats=data)
