from sqlalchemy.orm import Session
from app.models.tenant_user import TenantUser
from app.models.dtos import TenantUserCreate
from app.utils import hash_password


class TenantUserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_data: TenantUserCreate) -> TenantUser:
        

        user = TenantUser(
            email=user_data.email,
            tenant_schema=user_data.tenant_schema,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_email(self, email: str) -> TenantUser | None:
        return self.db.query(TenantUser).filter(TenantUser.email == email).first()
