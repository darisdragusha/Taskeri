from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from app.repositories.notification_repository import NotificationRepository
from app.utils import get_db
from app.models.dtos.notification_dtos import NotificationCreate, NotificationResponse

class NotificationController:
    """Controller class for handling notification operations."""

    def __init__(self, db_session: Session = Depends(get_db)):
        """
        Initialize the NotificationController.

        Args:
            db_session (Session): SQLAlchemy database session.
        """
        self.repository = NotificationRepository(db_session)

    def create_notification(self, notification_create: NotificationCreate) -> NotificationResponse:
        """
        Create a new notification.

        Args:
            notification_create (NotificationCreate): Data for the new notification.

        Returns:
            NotificationResponse: Created notification response.
        """
        try:
            notification = self.repository.create_notification(notification_create)
            return NotificationResponse.from_orm(notification)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")

    def get_notification(self, notification_id: int) -> NotificationResponse:
        """
        Retrieve a notification by ID.

        Args:
            notification_id (int): Notification ID.

        Returns:
            NotificationResponse: Retrieved notification response.
        """
        try:
            notification = self.repository.get_notification_by_id(notification_id)
            if not notification:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
            return NotificationResponse.from_orm(notification)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")

    def get_notifications_for_user(self, user_id: int, unread_only: bool = False) -> List[NotificationResponse]:
        """
        Retrieve all notifications for a specific user.

        Args:
            user_id (int): User ID.

        Returns:
            List[NotificationResponse]: List of notifications for the user.
        """
        try:
            notifications = self.repository.get_notifications_by_user(user_id)
            if unread_only:
                notifications = [n for n in notifications if not n.read_status]
                return [NotificationResponse.from_orm(n) for n in notifications]
            return [NotificationResponse.from_orm(n) for n in notifications]
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")

    def mark_notification_as_read(self, notification_id: int) -> NotificationResponse:
        """
        Mark a notification as read.

        Args:
            notification_id (int): Notification ID.

        Returns:
            NotificationResponse: Updated notification with read status set to True.
        """
        try:
            notification = self.repository.mark_as_read(notification_id)
            if not notification:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
            return NotificationResponse.from_orm(notification)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")

    def delete_notification(self, notification_id: int) -> dict:
        """
        Delete a notification by ID.

        Args:
            notification_id (int): Notification ID.

        Returns:
            dict: Success message.
        """
        try:
            success = self.repository.delete_notification(notification_id)
            if not success:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
            return {"detail": "Notification deleted"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")
