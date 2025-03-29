from sqlalchemy import Column, String, BigInteger, ForeignKey
from app.utils.db_utils import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    department_id = Column(BigInteger, ForeignKey("departments.id"))