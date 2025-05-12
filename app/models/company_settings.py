from sqlalchemy import Column, String, BigInteger, Integer, ForeignKey
from utils.db_utils import Base

class CompanySettings(Base):
    __tablename__ = "company_settings"
    __table_args__ = {"schema": None}


    company_id = Column(BigInteger, ForeignKey("companies.id"), primary_key=True)
    timezone = Column(String(50), nullable=False, default="UTC")
    work_hours_per_day = Column(Integer, default=8)
