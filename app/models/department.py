from sqlalchemy import Column, String, BigInteger, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from utils import Base
from .company import Company
class Department(Base):
    __tablename__ = "departments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    company_id = Column(BigInteger, ForeignKey('companies.id', ondelete="CASCADE"))
    created_at = Column(TIMESTAMP, default="CURRENT_TIMESTAMP")

    company = relationship("Company", backref="departments")
