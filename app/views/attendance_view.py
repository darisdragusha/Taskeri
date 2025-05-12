from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
from models.dtos.attendance_dtos import AttendanceResponse
from controllers.attendance_controller import AttendanceController
from models.attendance import Attendance
from utils.db_utils import get_db
from auth import auth_service

router = APIRouter(
    prefix="/attendance",
    tags=["attendance"],
    responses={404: {"description": "Not found"}}
)


@router.post("/check-in", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def check_in(
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Check in the current authenticated user.
    Automatically sets the current timestamp as check-in time.
    """
    controller = AttendanceController(db)
    return controller.create_attendance(user_id=current_user.get("user_id"))


@router.put("/check-out", response_model=AttendanceResponse)
def check_out(
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Check out the current authenticated user.
    Finds the most recent open attendance record and sets the check-out time.
    """
    controller = AttendanceController(db)
    return controller.close_attendance(user_id=current_user.get("user_id"))


@router.get("/my", response_model=List[AttendanceResponse])
def get_my_attendance(
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get all attendance records for the current authenticated user.
    """
    controller = AttendanceController(db)
    return controller.get_user_attendance(user_id=current_user.get("user_id"))

@router.get("/user/{user_id}", response_model=List[AttendanceResponse])
def get_my_attendance(
    request: Request,
    user_id: int, 
    db: Session = Depends(get_db),
):
    """
    Get all attendance records for the current authenticated user.
    """
    controller = AttendanceController(db)
    return controller.get_user_attendance(user_id)
