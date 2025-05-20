from sqlalchemy import Column, BigInteger, Text, TIMESTAMP, ForeignKey, func
from app.utils.db_utils import Base

class Comment(Base):
    __tablename__ = "comments"
    __table_args__ = {"schema": None}  # 👈 Important for schema-aware migration

    id = Column(BigInteger, primary_key=True)
    task_id = Column(BigInteger, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())