# app/models/user.py
from sqlalchemy import Column, String, Integer, BigInteger, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.utils import Base  
from .department import Department
from .team import Team
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    department_id = Column(BigInteger, ForeignKey('departments.id', ondelete="SET NULL"))
    team_id = Column(BigInteger, ForeignKey('teams.id', ondelete="SET NULL"))
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    department = relationship("Department", backref="users") 
    team = relationship("Team", backref="users")  
