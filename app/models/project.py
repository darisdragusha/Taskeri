from sqlalchemy import Column, String, Text, BigInteger, Date, Enum, TIMESTAMP, func
from app.utils.db_utils import Base

class Project(Base):
    __tablename__ = "projects"
    __table_args__ = {"schema": None} 

    id = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    status = Column(Enum("Not Started", "In Progress", "Completed", "On Hold"), default="Not Started")
    created_at = Column(TIMESTAMP, server_default=func.now())