from sqlalchemy import Column, String, BigInteger, Integer, Sequence
from app.utils.db_utils import Base

class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = {"schema": None}  
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)