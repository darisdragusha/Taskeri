from sqlalchemy import Column, BigInteger, String, TIMESTAMP, ForeignKey, func
from utils.db_utils import Base

class FileAttachment(Base):
    __tablename__ = "file_attachments"
    __table_args__ = {"schema": None}  # 👈 Important for schema-aware migration

    id = Column(BigInteger, primary_key=True)
    task_id = Column(BigInteger, ForeignKey("tasks.id"), nullable=False)
    file_path = Column(String(255), nullable=False)
    uploaded_at = Column(TIMESTAMP, server_default=func.now())