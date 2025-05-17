from sqlalchemy import Column, String, BigInteger, TIMESTAMP, ForeignKey, func
from app.utils.db_utils import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": None}  # 👈 Important for schema-aware migration

    id = Column(BigInteger, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    department_id = Column(BigInteger, ForeignKey("departments.id"), nullable=True)
    team_id = Column(BigInteger, ForeignKey("teams.id"), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())