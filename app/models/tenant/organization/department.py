from sqlalchemy import Column, String, BigInteger, ForeignKey
from app.utils.db_utils import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    company_id = Column(BigInteger, ForeignKey("companies.id"), nullable=False)