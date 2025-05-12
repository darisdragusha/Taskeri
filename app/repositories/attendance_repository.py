from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from models.attendance import Attendance


class AttendanceRepository:
    """Repository class for handling attendance-related database operations."""

    def __init__(self, db_session: Session):
        """
        Initialize the AttendanceRepository.

        Args:
            db_session (Session): SQLAlchemy database session.
        """
        self.db_session = db_session

    def create_attendance(self, user_id: int, check_in: datetime) -> Attendance:
        """
        Create a new attendance record with check-in time.

        Args:
            user_id (int): ID of the user
            check_in (datetime): Check-in timestamp

        Returns:
            Attendance: The created attendance record
        """
        try:
            attendance = Attendance(
                user_id=user_id,
                check_in=check_in
            )
            self.db_session.add(attendance)
            self.db_session.commit()
            self.db_session.refresh(attendance)
            return attendance
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e

    def get_attendance_for_user(self, user_id: int) -> List[Attendance]:
        """
        Get all attendance records for a specific user.

        Args:
            user_id (int): User ID

        Returns:
            List[Attendance]: List of attendance records
        """
        return self.db_session.query(Attendance).filter(
            Attendance.user_id == user_id
        ).order_by(Attendance.check_in.desc()).all()
        
    def close_open_attendance(self, user_id: int, check_out: datetime) -> Optional[Attendance]:
        """
        Find the latest open attendance (where check_out is NULL) and set check_out.

        Args:
            user_id (int): User ID
            check_out (datetime): Time to set as check_out

        Returns:
            Optional[Attendance]: Updated attendance record
        """
        try:
            open_attendance = self.db_session.query(Attendance).filter(
                Attendance.user_id == user_id,
                Attendance.check_out.is_(None)
            ).order_by(Attendance.check_in.desc()).first()

            if not open_attendance:
                return None

            open_attendance.check_out = check_out
            self.db_session.commit()
            self.db_session.refresh(open_attendance)
            return open_attendance
        except SQLAlchemyError as e:
            self.db_session.rollback()
            raise e
