from sqlalchemy import Column, BigInteger, ForeignKey
from app.utils.db_utils import Base

class RolePermission(Base):
    __tablename__ = "role_permissions"
    __table_args__ = {"schema": None}  

    role_id = Column(BigInteger, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)
    permission_id = Column(BigInteger, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)