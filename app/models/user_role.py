from sqlalchemy import Column, BigInteger, ForeignKey
from app.utils.db_utils import Base

class UserRole(Base):
    __tablename__ = "user_roles"
    __table_args__ = {"schema": None}

    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    role_id = Column(BigInteger, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True)