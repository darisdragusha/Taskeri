from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CompanyCreate(BaseModel):
    name: str
    industry: Optional[str] = None
    country: Optional[str] = None

class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None

class CompanyResponse(BaseModel):
    id: int
    name: str
    industry: Optional[str]
    country: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
        orm_mode = True
