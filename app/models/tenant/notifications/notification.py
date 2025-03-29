from sqlalchemy import Column, BigInteger, Text, Boolean, TIMESTAMP, ForeignKey, func
from app.utils.db_utils import Base

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=False)
    read_status = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())