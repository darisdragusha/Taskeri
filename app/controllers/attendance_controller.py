from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from typing import List

from repositories.attendance_repository import AttendanceRepository
from models.attendance import Attendance
from utils import get_db


class AttendanceController:
    """Controller class for handling attendance operations."""

    def __init__(self, db_session: Session = Depends(get_db)):
        self.repository = AttendanceRepository(db_session)

    def create_attendance(self, user_id: int) -> Attendance:
        try:
            now = datetime.utcnow()
            return self.repository.create_attendance(user_id=user_id, check_in=now)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error during check-in: {str(e)}"
            )

    def close_attendance(self, user_id: int) -> Attendance:
        try:
            now = datetime.utcnow()
            attendance = self.repository.close_open_attendance(user_id=user_id, check_out=now)
            if not attendance:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No open attendance record found for this user"
                )
            return attendance
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error during check-out: {str(e)}"
            )
        
    def get_user_attendance(self, user_id: int) -> List[Attendance]:
        """
        Retrieve all attendance records for a given user.

        Args:
            user_id (int): ID of the user

        Returns:
            List[Attendance]: List of attendance records
        """
        try:
            return self.repository.get_attendance_for_user(user_id)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error retrieving attendance: {str(e)}"
            )