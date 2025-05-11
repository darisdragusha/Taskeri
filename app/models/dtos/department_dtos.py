from pydantic import BaseModel
from typing import Optional


class DepartmentCreate(BaseModel):
    name: str
    company_id: int


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    company_id: Optional[int] = None


class DepartmentResponse(BaseModel):
    id: int
    name: str
    company_id: int

    class Config:
        from_attributes = True
        orm_mode = True
