from sqlalchemy import Column, BigInteger, ForeignKey
from utils.db_utils import Base

class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = {"schema": None}  # 👈 Important for schema-aware migration

    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    role_id = Column(BigInteger, ForeignKey("roles.id"), primary_key=True)