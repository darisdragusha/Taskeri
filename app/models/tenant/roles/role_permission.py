from sqlalchemy import Column, BigInteger, ForeignKey
from app.utils.db_utils import Base

class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_id = Column(BigInteger, ForeignKey("roles.id"), primary_key=True)
    permission_id = Column(BigInteger, ForeignKey("permissions.id"), primary_key=True)