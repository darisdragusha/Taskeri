from sqlalchemy import Column, BigInteger, Enum, Date, ForeignKey
from app.utils.db_utils import Base

class LeaveRequest(Base):
    __tablename__ = "leave_requests"
    __table_args__ = {"schema": None}

    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    leave_type = Column(Enum("Vacation", "Sick Leave", "Personal", "Other"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(Enum("Pending", "Approved", "Rejected"), default="Pending")