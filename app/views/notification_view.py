from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from app.models.dtos.notification_dtos import NotificationCreate, NotificationResponse
from app.controllers.notification_controller import NotificationController
from app.utils import get_db
from app.auth import auth_service

router = APIRouter(prefix="/notifications", tags=["Notifications"])

def get_notification_controller(db: Session = Depends(get_db)) -> NotificationController:
    return NotificationController(db)

@router.post("/", response_model=NotificationResponse)
def create_notification(
    data: NotificationCreate,
    request: Request,
    db: Session = Depends(get_db),
    controller: NotificationController = Depends(get_notification_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Create a new notification.
    Permission check required for 'create_notification'.
    """
    return controller.create_notification(data)

@router.get("/user/{user_id}", response_model=List[NotificationResponse])
def get_notifications_for_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    controller: NotificationController = Depends(get_notification_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get all notifications for a given user.
    Permission check required for 'read_notification'.
    """
    return controller.get_notifications_for_user(user_id)

@router.get("/{notification_id}", response_model=NotificationResponse)
def get_notification(
    notification_id: int,
    request: Request,
    db: Session = Depends(get_db),
    controller: NotificationController = Depends(get_notification_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get a notification by ID.
    Permission check required for 'read_notification'.
    """
    return controller.get_notification(notification_id)

@router.put("/{notification_id}/read", response_model=NotificationResponse)
def mark_notification_read(
    notification_id: int,
    request: Request,
    db: Session = Depends(get_db),
    controller: NotificationController = Depends(get_notification_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Mark notification as read.
    Permission check required for 'update_notification'.
    """
    return controller.mark_notification_as_read(notification_id)

@router.delete("/{notification_id}", response_model=dict)
def delete_notification(
    notification_id: int,
    request: Request,
    db: Session = Depends(get_db),
    controller: NotificationController = Depends(get_notification_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Delete a notification by ID.
    Permission check required for 'delete_notification'.
    """
    return controller.delete_notification(notification_id)

from fastapi import Query

@router.get("/get/me", response_model=List[NotificationResponse])
def get_my_notifications(
    request: Request,
    unread_only: bool = Query(False),
    db: Session = Depends(get_db),
    controller: NotificationController = Depends(get_notification_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get all notifications for the current user.
    Supports filtering by unread_only.
    Permission check required for 'read_notification'.
    """
    return controller.get_notifications_for_user(
        user_id=current_user["user_id"],
        unread_only=unread_only
    )
