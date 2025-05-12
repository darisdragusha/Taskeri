from pydantic import BaseModel, Field
from typing import Optional

class CompanySettingsBase(BaseModel):
    timezone: str = Field(default="UTC", max_length=50)
    work_hours_per_day: int = Field(default=8, ge=1, le=24)

class CompanySettingsCreate(CompanySettingsBase):
    company_id: int

class CompanySettingsUpdate(BaseModel):
    timezone: Optional[str] = Field(default=None, max_length=50)
    work_hours_per_day: Optional[int] = Field(default=None, ge=1, le=24)

class CompanySettingsResponse(CompanySettingsBase):
    company_id: int

    class Config:
        orm_mode = True