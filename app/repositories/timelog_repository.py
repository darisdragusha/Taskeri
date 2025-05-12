from sqlalchemy.orm import Session
from typing import List, Optional, Tuple
from sqlalchemy import desc
from datetime import datetime

from models.time_log import TimeLog  # Adjust the import path if needed
from models.dtos.timelog_dtos import TimeLogCreate, TimeLogUpdate  # You must define these DTOs


class TimeLogRepository:
    """Repository class for handling time log-related database operations."""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    from datetime import timedelta

    def create_time_log(self, data: TimeLogCreate) -> TimeLog:
        """Create a new time log entry with duration calculated automatically."""
        try:
            duration = int((data.end_time - data.start_time).total_seconds() / 60)

            time_log = TimeLog(
                user_id=data.user_id,
                task_id=data.task_id,
                start_time=data.start_time,
                end_time=data.end_time,
                duration=duration,
            )
            self.db_session.add(time_log)
            self.db_session.commit()
            self.db_session.refresh(time_log)
            return time_log
        except Exception as e:
            self.db_session.rollback()
            raise e


    def get_time_log_by_id(self, time_log_id: int) -> Optional[TimeLog]:
        """Get a time log by its ID."""
        return self.db_session.query(TimeLog).filter(TimeLog.id == time_log_id).first()

    def get_time_logs_by_user(self, user_id: int) -> List[TimeLog]:
        """Get all time logs for a specific user."""
        return self.db_session.query(TimeLog).filter(TimeLog.user_id == user_id).order_by(desc(TimeLog.start_time)).all()

    def get_time_logs_by_task(self, task_id: int) -> List[TimeLog]:
        """Get all time logs for a specific task."""
        return self.db_session.query(TimeLog).filter(TimeLog.task_id == task_id).order_by(desc(TimeLog.start_time)).all()

    def update_time_log(self, time_log_id: int, data: TimeLogUpdate) -> Optional[TimeLog]:
        """Update an existing time log."""
        try:
            time_log = self.get_time_log_by_id(time_log_id)
            if not time_log:
                return None

            time_log.start_time = data.start_time
            time_log.end_time = data.end_time
            time_log.duration = data.duration

            self.db_session.commit()
            self.db_session.refresh(time_log)
            return time_log
        except Exception as e:
            self.db_session.rollback()
            raise e

    def delete_time_log(self, time_log_id: int) -> bool:
        """Delete a time log by ID."""
        try:
            time_log = self.get_time_log_by_id(time_log_id)
            if not time_log:
                return False

            self.db_session.delete(time_log)
            self.db_session.commit()
            return True
        except Exception as e:
            self.db_session.rollback()
            raise e
        

    def get_user_logs_by_time_range(self, user_id: int, start: datetime, end: datetime) -> List[TimeLog]:
        """
        Get logs for a user where start_time is within the given range.
        """
        return self.db_session.query(TimeLog).filter(
            TimeLog.user_id == user_id,
            TimeLog.start_time >= start,
            TimeLog.start_time <= end
        ).order_by(TimeLog.start_time).all()

