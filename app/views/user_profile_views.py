from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.controllers.user_profile_controller import UserProfileController
from app.models.dtos.user_profile_dtos import UserProfileCreate, UserProfileUpdate, UserProfileResponse
from app.utils import get_db
from typing import Optional
from app.auth import auth_service

router = APIRouter(prefix="/profiles", tags=["User Profiles"])

def get_user_profile_controller(db: Session = Depends(get_db)) -> UserProfileController:
    return UserProfileController(db)

@router.post("/", response_model=UserProfileResponse)
def create_user_profile(
    data: UserProfileCreate,
    request: Request,
    db: Session = Depends(get_db),
    controller: UserProfileController = Depends(get_user_profile_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Create a new user profile.

    Business logic:
    - Only existing users can have a profile
    - Each user can have only one profile
    """
    return controller.create_profile(data)

@router.get("/{user_id}", response_model=UserProfileResponse)
def get_user_profile(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    controller: UserProfileController = Depends(get_user_profile_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Retrieve a user's profile by their ID.

    Business logic:
    - Must return 404 if profile does not exist
    """
    profile = controller.get_profile_by_user_id(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile

@router.put("/{user_id}", response_model=UserProfileResponse)
def update_user_profile(
    user_id: int,
    data: UserProfileUpdate,
    request: Request,
    db: Session = Depends(get_db),
    controller: UserProfileController = Depends(get_user_profile_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Update a user profile by user ID.

    Business logic:
    - User must already have a profile
    - Only provided fields will be updated
    """
    profile = controller.update_profile(user_id, data)
    if not profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile

@router.delete("/{user_id}", response_model=dict)
def delete_user_profile(
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    controller: UserProfileController = Depends(get_user_profile_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Delete a user profile by user ID.

    Business logic:
    - Profile must exist
    - Deletion may be soft or hard depending on policy
    """
    success = controller.delete_profile(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User profile not found")
    return {"detail": "User profile deleted"}
