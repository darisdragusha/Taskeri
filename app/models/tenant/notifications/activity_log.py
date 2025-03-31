from sqlalchemy import Column, BigInteger, Text, TIMESTAMP, ForeignKey, func
from app.utils.db_utils import Base

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    __table_args__ = {"schema": None}  # 👈 Important for schema-aware migration

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    action = Column(Text, nullable=False)
    timestamp = Column(TIMESTAMP, server_default=func.now())