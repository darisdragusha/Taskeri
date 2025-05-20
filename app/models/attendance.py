from sqlalchemy import Column, BigInteger, TIMESTAMP, ForeignKey
from app.utils.db_utils import Base

class Attendance(Base):
    __tablename__ = "attendance"
    __table_args__ = {"schema": None}

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    check_in = Column(TIMESTAMP, nullable=False)
    check_out = Column(TIMESTAMP)