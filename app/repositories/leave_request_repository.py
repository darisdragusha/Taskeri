from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.leave_request import LeaveRequest

class LeaveRequestRepository:
    """Repository class for handling leave request-related database operations."""

    def __init__(self, db_session: Session):
        """
        Initialize the LeaveRequestRepository.

        Args:
            db_session (Session): SQLAlchemy database session.
        """
        self.db_session = db_session

    def create_leave_request(
        self,
        user_id: int,
        leave_type: str,
        start_date,
        end_date,
        status: str = "Pending"
    ) -> LeaveRequest:
        """
        Create a new leave request.

        Args:
            user_id (int): ID of the user requesting leave
            leave_type (str): Type of leave
            start_date (date): Start date of the leave
            end_date (date): End date of the leave
            status (str): Status of the leave (Pending, Approved, Rejected)

        Returns:
            LeaveRequest: The newly created leave request object
        """
        try:
            leave = LeaveRequest(
                user_id=user_id,
                leave_type=leave_type,
                start_date=start_date,
                end_date=end_date,
                status=status
            )
            self.db_session.add(leave)
            self.db_session.commit()
            self.db_session.refresh(leave)
            return leave
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_leave_request_by_id(self, leave_id: int) -> Optional[LeaveRequest]:
        """
        Retrieve a leave request by ID.

        Args:
            leave_id (int): Leave request ID.

        Returns:
            Optional[LeaveRequest]: Leave request if found, otherwise None.
        """
        return self.db_session.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()

    def get_leave_requests_by_user(self, user_id: int) -> List[LeaveRequest]:
        """
        Retrieve all leave requests submitted by a specific user.

        Args:
            user_id (int): ID of the user.

        Returns:
            List[LeaveRequest]: List of leave requests.
        """
        return self.db_session.query(LeaveRequest).filter(LeaveRequest.user_id == user_id).all()

    def update_leave_status(self, leave_id: int, status: str) -> Optional[LeaveRequest]:
        """
        Update the status of a leave request.

        Args:
            leave_id (int): Leave request ID
            status (str): New status (Pending, Approved, Rejected)

        Returns:
            Optional[LeaveRequest]: Updated leave request object
        """
        try:
            leave = self.get_leave_request_by_id(leave_id)
            if not leave:
                return None
            leave.status = status
            self.db_session.commit()
            self.db_session.refresh(leave)
            return leave
        except Exception as e:
            self.db_session.rollback()
            raise e

    def delete_leave_request(self, leave_id: int) -> Optional[LeaveRequest]:
        """
        Delete a leave request by ID.

        Args:
            leave_id (int): Leave request ID

        Returns:
            Optional[LeaveRequest]: Deleted leave request object
        """
        try:
            leave = self.get_leave_request_by_id(leave_id)
            if leave:
                self.db_session.delete(leave)
                self.db_session.commit()
                return leave
            return None
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_leave_statistics(self) -> dict:
        """
        Get summary statistics of leave requests.

        Returns:
            dict: Counts of leave requests by status.
        """
        statuses = ["Pending", "Approved", "Rejected"]
        result = {}
        for status in statuses:
            count = self.db_session.query(func.count(LeaveRequest.id)).filter(LeaveRequest.status == status).scalar()
            result[status] = count
        return result
