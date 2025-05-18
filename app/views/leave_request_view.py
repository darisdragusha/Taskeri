from fastapi import APIRouter, Depends, status, Query, Path, Request, HTTPException
from app.controllers.leave_request_controller import LeaveRequestController
from app.models.dtos.leave_request_dtos import LeaveRequestCreate, LeaveRequestResponse, LeaveRequestListResponse
from typing import List, Literal, Dict
from sqlalchemy.orm import Session
from app.auth import auth_service
from app.utils.db_utils import get_db


router = APIRouter(
    prefix="/leave-requests",
    tags=["Leave Requests"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=LeaveRequestResponse, status_code=status.HTTP_201_CREATED)
def create_leave_request(
    leave_data: LeaveRequestCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Create a new leave request for the authenticated user.

    The user_id will be automatically set to the current authenticated user.
    """
    user_id = current_user.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User authentication failed"
        )

    controller = LeaveRequestController(db)
    return controller.create_leave_request(leave_data, user_id=user_id)



@router.get("/{leave_id}", response_model=LeaveRequestResponse)
async def get_leave_request(
    leave_id: int,
    controller: LeaveRequestController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get a leave request by ID.
    """
    return controller.get_leave_request(leave_id)


@router.get("/user/{user_id}", response_model=List[LeaveRequestResponse])
async def get_leave_requests_by_user(
    user_id: int,
    controller: LeaveRequestController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get all leave requests submitted by a specific user.
    """
    return controller.get_leave_requests_by_user(user_id)


@router.patch("/{leave_id}/status", response_model=LeaveRequestResponse)
async def update_leave_status(
    leave_id: int,
    status: Literal["Approved", "Rejected"] = Query(..., description="New status for the leave request"),
    controller: LeaveRequestController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Update the status of a leave request.
    """
    return controller.update_leave_status(leave_id, status)


@router.delete("/{leave_id}", response_model=Dict[str, str])
async def delete_leave_request(
    leave_id: int,
    controller: LeaveRequestController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Delete a leave request by ID.
    """
    return controller.delete_leave_request(leave_id)


@router.get("/", response_model=LeaveRequestListResponse)
async def get_paginated_leave_requests(
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    controller: LeaveRequestController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get a paginated list of all leave requests.

    Permission requirements (handled by middleware):
    - Admin/HR roles typically have access to all leave requests
    """
    return controller.get_paginated_leave_requests(page=page, page_size=page_size)