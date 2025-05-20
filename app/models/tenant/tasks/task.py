from sqlalchemy import Column, String, Text, BigInteger, Date, Enum, TIMESTAMP, ForeignKey, func
from app.utils.db_utils import Base

class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = {"schema": None}  # 👈 Important for schema-aware migration

    id = Column(BigInteger, primary_key=True)
    project_id = Column(BigInteger, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    priority = Column(Enum("Low", "Medium", "High"), default="Medium")
    status = Column(Enum("To Do", "In Progress", "Technical Review", "Done"), default="To Do")
    due_date = Column(Date)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())