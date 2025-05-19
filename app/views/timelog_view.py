from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Dict

from app.models.dtos.timelog_dtos import TimeLogCreate, TimeLogUpdate, TimeLogResponse
from app.controllers.timelog_controller import TimeLogController
from app.utils.db_utils import get_db
from datetime import datetime
from app.auth import auth_service  # Assumes JWT or session-based auth that returns current user info

router = APIRouter(
    prefix="/time-logs",
    tags=["time_logs"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=TimeLogResponse, status_code=status.HTTP_201_CREATED)
def create_time_log(
    data: TimeLogCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Create a new time log. The user is automatically set from the logged-in user.
    """
    controller = TimeLogController(db)
    return controller.create_time_log(user_id=current_user["user_id"], data=data)


@router.get("/{time_log_id}", response_model=TimeLogResponse)
def get_time_log(
    time_log_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get a time log by ID.
    """
    controller = TimeLogController(db)
    log = controller.get_time_log(time_log_id)
    if not log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Time log with ID {time_log_id} not found"
        )
    return log


@router.get("/task/{task_id}", response_model=List[TimeLogResponse])
def get_time_logs_by_task(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get all time logs associated with a specific task.
    """
    controller = TimeLogController(db)
    return controller.get_time_logs_by_task(task_id)


@router.get("/my", response_model=List[TimeLogResponse])
def get_my_time_logs(
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get all time logs created by the current user.
    """
    controller = TimeLogController(db)
    return controller.get_time_logs_by_user(current_user["user_id"])


@router.put("/{time_log_id}", response_model=TimeLogResponse)
def update_time_log(
    time_log_id: int,
    data: TimeLogUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Update a time log. The duration will be recalculated automatically.
    """
    controller = TimeLogController(db)
    return controller.update_time_log(time_log_id, data)


@router.delete("/{time_log_id}", response_model=Dict[str, str])
def delete_time_log(
    time_log_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Delete a time log entry.
    """
    controller = TimeLogController(db)
    controller.delete_time_log(time_log_id)
    return {"message": "Time log deleted successfully"}

@router.get("/user/{user_id}/by-time", response_model=List[TimeLogResponse])
def get_user_time_logs_by_time_range(
    user_id: int,
    start_date: datetime,
    end_date: datetime,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get all time logs for a specific user within a date range.
    """
    controller = TimeLogController(db)
    return controller.get_user_logs_by_time_range(user_id, start_date, end_date)
