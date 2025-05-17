from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Literal

from app.repositories.leave_request_repository import LeaveRequestRepository
from app.models.leave_request import LeaveRequest
from app.models.dtos.leave_request_dtos import LeaveRequestCreate, LeaveRequestResponse
from app.utils import get_db


class LeaveRequestController:
    """Controller class for handling leave request operations."""

    def __init__(self, db_session: Session = Depends(get_db)):
        """
        Initialize the LeaveRequestController.

        Args:
            db_session (Session): SQLAlchemy database session.
        """
        self.repository = LeaveRequestRepository(db_session)

    def create_leave_request(
        self,
        request: LeaveRequestCreate,
        user_id: int
    ) -> LeaveRequestResponse:
        try:
            leave = self.repository.create_leave_request(
                user_id=user_id,
                leave_type=request.leave_type,
                start_date=request.start_date,
                end_date=request.end_date,
                status="Pending"
            )
            return LeaveRequestResponse.from_orm(leave)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )

    def get_leave_request(self, leave_id: int) -> LeaveRequestResponse:
        """
        Get a leave request by ID.

        Args:
            leave_id (int): Leave request ID.

        Returns:
            LeaveRequestResponse: Leave request response.
        """
        try:
            leave = self.repository.get_leave_request_by_id(leave_id)
            if not leave:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Leave request not found"
                )
            return LeaveRequestResponse.from_orm(leave)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )

    def get_leave_requests_by_user(self, user_id: int) -> List[LeaveRequestResponse]:
        """
        Get all leave requests by a specific user.

        Args:
            user_id (int): User ID.

        Returns:
            List[LeaveRequestResponse]: List of leave requests.
        """
        try:
            leaves = self.repository.get_leave_requests_by_user(user_id)
            return [LeaveRequestResponse.from_orm(lr) for lr in leaves]
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )

    def update_leave_status(
        self,
        leave_id: int,
        status: Literal["Approved", "Rejected"]
    ) -> LeaveRequestResponse:
        """
        Update the status of a leave request.

        Args:
            leave_id (int): Leave request ID.
            status (str): New status ("Approved" or "Rejected").

        Returns:
            LeaveRequestResponse: Updated leave request.
        """
        if status not in ["Approved", "Rejected"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid status"
            )

        try:
            leave = self.repository.update_leave_status(leave_id, status)
            if not leave:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Leave request not found"
                )
            return LeaveRequestResponse.from_orm(leave)
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

    def delete_leave_request(self, leave_id: int) -> Dict[str, str]:
        """
        Delete a leave request.

        Args:
            leave_id (int): Leave request ID.

        Returns:
            Dict[str, str]: Success message.
        """
        try:
            leave = self.repository.delete_leave_request(leave_id)
            if not leave:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Leave request not found"
                )
            return {"message": "Leave request deleted successfully"}
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
