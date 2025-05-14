from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from pydantic import EmailStr


class TenantUserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    tenant_schema: str

class TenantUserOut(BaseModel):
    id: int
    email: EmailStr
    tenant_schema: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

