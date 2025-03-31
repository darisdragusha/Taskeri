from sqlalchemy import Column, String, BigInteger
from app.utils.db_utils import Base

class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = {"schema": None}  # 👈 Important for schema-aware migration

    id = Column(BigInteger, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)