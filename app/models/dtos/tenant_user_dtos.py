from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
import re


class TenantUserCreate(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    company_name: str
    tenant_schema: Optional[str] = None
    
    def model_post_init(self, __context):
        # Generate tenant_schema from company_name if not provided
        if not self.tenant_schema and self.company_name:
            # Convert company name to lowercase, replace spaces with underscores, remove non-alphanumeric
            self.tenant_schema = re.sub(r'[^a-z0-9_]', '', self.company_name.lower().replace(' ', '_'))

class TenantUserOut(BaseModel):
    id: int
    email: EmailStr
    tenant_schema: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

