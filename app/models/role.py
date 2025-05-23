from sqlalchemy import Column, String, BigInteger
from app.utils.db_utils import Base

class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": None}  

    id = Column(BigInteger, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)