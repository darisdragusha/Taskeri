from sqlalchemy import Column, BigInteger, TIMESTAMP, ForeignKey
from app.utils.db_utils import Base

class Attendance(Base):
    __tablename__ = "attendance"
    __table_args__ = {"schema": None}  # 👈 Important for schema-aware migration

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    check_in = Column(TIMESTAMP, nullable=False)
    check_out = Column(TIMESTAMP)