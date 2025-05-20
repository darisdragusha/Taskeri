from sqlalchemy import Column, BigInteger, TIMESTAMP, ForeignKey, PrimaryKeyConstraint, func
from app.utils.db_utils import Base

class TaskAssignment(Base):
    __tablename__ = "task_assignments"
    __table_args__ = (
        PrimaryKeyConstraint("task_id", "user_id"),
        {"schema": None}  # must be at the end as a dict
    )

    task_id = Column(BigInteger, ForeignKey("tasks.id", ondelete="CASCADE"))
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    assigned_at = Column(TIMESTAMP, server_default=func.now())
