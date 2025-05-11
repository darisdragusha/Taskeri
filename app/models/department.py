from sqlalchemy import Column, String, BigInteger, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from utils import Base

class Department(Base):
    __tablename__ = "departments"

    id = Column(BigInteger, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    company_id = Column(BigInteger, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))

    company = relationship("Company", back_populates="departments")
