from sqlalchemy import Column, String, Text, BigInteger, ForeignKey
from app.utils.db_utils import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"
    __table_args__ = {"schema": None}  # 👈 Important for schema-aware migration

    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    position = Column(String(100))
    skills = Column(Text)
    bio = Column(Text)
    profile_pic = Column(String(255))