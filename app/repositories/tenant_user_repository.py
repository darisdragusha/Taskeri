from sqlalchemy.orm import Session
from models.tenant_user import TenantUser
from models.dtos.tenant_user_dtos import TenantUserCreate
from utils.auth_utils import hash_password


class TenantUserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_data: TenantUserCreate) -> TenantUser:
        hashed_pw = hash_password(user_data.password) 

        user = TenantUser(
            email=user_data.email,
            password_hash=hashed_pw,
            tenant_schema=user_data.tenant_schema,
            role=user_data.role,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_email(self, email: str) -> TenantUser | None:
        return self.db.query(TenantUser).filter(TenantUser.email == email).first()
