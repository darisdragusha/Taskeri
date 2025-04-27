from sqlalchemy import Column, String, BigInteger, ForeignKey
from utils.db_utils import Base

class Team(Base):
    __tablename__ = "teams"
    __table_args__ = {"schema": None}  # 👈 Important for schema-aware migration

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    department_id = Column(BigInteger, ForeignKey("departments.id"))