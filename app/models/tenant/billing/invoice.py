from sqlalchemy import Column, BigInteger, DECIMAL, TIMESTAMP, Enum, ForeignKey, func
from app.utils.db_utils import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(BigInteger, primary_key=True)
    company_id = Column(BigInteger, ForeignKey("companies.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    issued_at = Column(TIMESTAMP, server_default=func.now())
    status = Column(Enum("Pending", "Paid"), default="Pending")