from sqlalchemy import Column, String, BigInteger, TIMESTAMP, func
from app.utils.db_utils import Base

class Company(Base):
    __tablename__ = "companies"
    __table_args__ = {"schema": None}  # 👈 Important for schema-aware migration

    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    industry = Column(String(100))
    country = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now())