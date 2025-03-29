from sqlalchemy import Column, BigInteger, String, TIMESTAMP, ForeignKey, func
from app.utils.db_utils import Base

class FileAttachment(Base):
    __tablename__ = "file_attachments"

    id = Column(BigInteger, primary_key=True)
    task_id = Column(BigInteger, ForeignKey("tasks.id"), nullable=False)
    file_path = Column(String(255), nullable=False)
    uploaded_at = Column(TIMESTAMP, server_default=func.now())