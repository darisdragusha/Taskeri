from sqlalchemy import Column, String, BigInteger
from app.utils.db_utils import Base

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)