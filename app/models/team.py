# app/models/team.py
from sqlalchemy import Column, String, BigInteger, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.utils import Base
from .department import Department
class Team(Base):
    __tablename__ = "teams"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    department_id = Column(BigInteger, ForeignKey("departments.id"))

    department = relationship("Department", backref="teams")
