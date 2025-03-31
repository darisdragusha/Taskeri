from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic import EmailStr


class TenantUserCreate(BaseModel):
    email: EmailStr
    password: str
    tenant_schema: str
    role: str  # Admin, Manager, Employee

class TenantUserOut(BaseModel):
    id: int
    email: EmailStr
    tenant_schema: str
    role: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

