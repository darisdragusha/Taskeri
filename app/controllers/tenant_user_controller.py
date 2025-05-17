from app.models.dtos import TenantUserCreate, TenantUserOut
from app.repositories import TenantUserRepository
from app.services.tenant_provisioning import create_new_tenant
from sqlalchemy.orm import Session
from fastapi import HTTPException


class TenantUserController:
    def __init__(self, db: Session):
        self.repo = TenantUserRepository(db)

    def register_tenant_user(self, user_data: TenantUserCreate) -> TenantUserOut:
        if self.repo.get_by_email(user_data.email):
            raise HTTPException(status_code=400, detail="Email already exists.")

        create_new_tenant(self.repo.db, user_data.tenant_schema)
        user = self.repo.create(user_data)

        return TenantUserOut.model_validate(user)
