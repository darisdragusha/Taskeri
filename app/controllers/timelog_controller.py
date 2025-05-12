from typing import Optional, List
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

from models.dtos.timelog_dtos import TimeLogCreate, TimeLogUpdate, TimeLogResponse
from repositories.timelog_repository import TimeLogRepository
from models.time_log import TimeLog
from utils.db_utils import get_db


class TimeLogController:
    """Controller class for handling time log-related operations."""

    def __init__(self, db_session: Session = Depends(get_db)):
        self.repository = TimeLogRepository(db_session)

    def create_time_log(self, data: TimeLogCreate) -> TimeLogResponse:
        """Create a new time log entry with duration calculated."""
        try:
            time_log = self.repository.create_time_log(data)
            return self._map_to_response(time_log)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred"
            )

    def get_time_log(self, time_log_id: int) -> Optional[TimeLogResponse]:
        """Get a time log entry by ID."""
        try:
            time_log = self.repository.get_time_log_by_id(time_log_id)
            if not time_log:
                return None
            return self._map_to_response(time_log)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )

    def get_time_logs_by_user(self, user_id: int) -> List[TimeLogResponse]:
        """Get all time logs for a specific user."""
        try:
            logs = self.repository.get_time_logs_by_user(user_id)
            return [self._map_to_response(log) for log in logs]
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )

    def get_time_logs_by_task(self, task_id: int) -> List[TimeLogResponse]:
        """Get all time logs for a specific task."""
        try:
            logs = self.repository.get_time_logs_by_task(task_id)
            return [self._map_to_response(log) for log in logs]
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )

    def update_time_log(self, time_log_id: int, data: TimeLogUpdate) -> TimeLogResponse:
        """Update an existing time log (recalculate duration)."""
        try:
            updated_log = self.repository.update_time_log(time_log_id, data)
            if not updated_log:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Time log with ID {time_log_id} not found"
                )
            return self._map_to_response(updated_log)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )

    def delete_time_log(self, time_log_id: int) -> bool:
        """Delete a time log entry."""
        try:
            success = self.repository.delete_time_log(time_log_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Time log with ID {time_log_id} not found"
                )
            return True
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )

    def _map_to_response(self, log: TimeLog) -> TimeLogResponse:
        """Map TimeLog model to response DTO."""
        return TimeLogResponse(
            id=log.id,
            user_id=log.user_id,
            task_id=log.task_id,
            start_time=log.start_time,
            end_time=log.end_time,
            duration=log.duration
        )
    
    def get_user_logs_by_time_range(self, user_id: int, start: datetime, end: datetime) -> List[TimeLogResponse]:
        """
        Get all time logs for a user within a specific date range.
        """
        try:
            logs = self.repository.get_user_logs_by_time_range(user_id, start, end)
            return [self._map_to_response(log) for log in logs]
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
