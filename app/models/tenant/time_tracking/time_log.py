from sqlalchemy import Column, BigInteger, TIMESTAMP, Integer, ForeignKey
from app.utils.db_utils import Base

class TimeLog(Base):
    __tablename__ = "time_logs"
    __table_args__ = {"schema": None}  # 👈 Important for schema-aware migration

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    task_id = Column(BigInteger, ForeignKey("tasks.id"), nullable=False)
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP)
    duration = Column(Integer)  # in minutes