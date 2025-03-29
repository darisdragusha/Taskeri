from sqlalchemy import Column, BigInteger, Text, TIMESTAMP, ForeignKey, func
from app.utils.db_utils import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(BigInteger, primary_key=True)
    task_id = Column(BigInteger, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())