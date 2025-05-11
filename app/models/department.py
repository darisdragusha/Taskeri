from sqlalchemy import Column, String, BigInteger, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from utils import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    company_id = Column(BigInteger, ForeignKey("companies.id"), nullable=False)
    company = relationship("Company", backref="departments")