from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.notification import Notification
from app.models.dtos.notification_dtos import NotificationCreate
from typing import Optional, List

class NotificationRepository:
    """Repository class for handling database operations related to notifications."""

    def __init__(self, db: Session):
        """
        Initialize the NotificationRepository.

        Args:
            db (Session): SQLAlchemy database session.
        """
        self.db = db

    def create_notification(self, notification_create: NotificationCreate) -> Notification:
        """
        Create a new notification in the database.

        Args:
            notification_create (NotificationCreate): Data for the new notification.

        Returns:
            Notification: Created notification instance.
        """
        new_notification = Notification(
            user_id=notification_create.user_id,
            message=notification_create.message,
            read_status=notification_create.read_status or False
        )
        self.db.add(new_notification)
        self.db.commit()
        self.db.refresh(new_notification)
        return new_notification

    def get_notification_by_id(self, notification_id: int) -> Optional[Notification]:
        """
        Retrieve a notification by its ID.

        Args:
            notification_id (int): Notification ID.

        Returns:
            Optional[Notification]: Notification instance if found, otherwise None.
        """
        return self.db.query(Notification).filter(Notification.id == notification_id).first()

    def get_notifications_by_user(self, user_id: int) -> List[Notification]:
        """
        Retrieve all notifications for a specific user.

        Args:
            user_id (int): User ID.

        Returns:
            List[Notification]: List of notifications for the user.
        """
        return self.db.query(Notification).filter(Notification.user_id == user_id).all()

    def mark_as_read(self, notification_id: int) -> Optional[Notification]:
        """
        Mark a specific notification as read.

        Args:
            notification_id (int): Notification ID.

        Returns:
            Optional[Notification]: Updated notification instance if found, otherwise None.
        """
        notification = self.get_notification_by_id(notification_id)
        if notification:
            notification.read_status = True
            self.db.commit()
            self.db.refresh(notification)
        return notification

    def delete_notification(self, notification_id: int) -> bool:
        """
        Delete a notification by its ID.

        Args:
            notification_id (int): Notification ID.

        Returns:
            bool: True if deletion was successful, False if the notification was not found.
        """
        notification = self.get_notification_by_id(notification_id)
        if notification:
            self.db.delete(notification)
            self.db.commit()
            return True
        return False
