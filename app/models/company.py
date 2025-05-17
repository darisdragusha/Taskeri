from sqlalchemy import Column, String, Integer, BigInteger, TIMESTAMP, func
from app.utils import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    industry = Column(String(100))
    country = Column(String(100))
    created_at = Column(TIMESTAMP, server_default=func.now())
