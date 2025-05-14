# app/views/user_view.py
from fastapi import HTTPException, status, APIRouter, Depends, Request
from controllers import UserController
from models.dtos import UserCreate, UserUpdate, UserResponse
from sqlalchemy.sql import text
from utils.db_utils import get_db 
from auth import auth_service


router = APIRouter(tags=["User"])

@router.post("/users/create", response_model=UserResponse)
async def create_user(
    user_create: UserCreate,
    request: Request,
    controller: UserController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
) -> UserResponse:
    """
    Endpoint to create a new user.
    Requires the 'create_user' permission (handled by middleware).
    """
    return controller.create_user(user_create, current_user)


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    request: Request,
    controller: UserController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
) -> UserResponse:
    """
    Endpoint to get a user by ID.
    
    Permission requirements (handled by middleware):
    - 'read_user' permission (for own profile)
    - 'read_any_user' permission (for any profile)
    
    Business logic:
    - Users can always view their own profile
    - Viewing other profiles requires the 'read_any_user' permission
    """
    
    return controller.get_user(user_id)

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    request: Request,
    controller: UserController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
) -> UserResponse:
    """
    Endpoint to update a user.
    
    Permission requirements (handled by middleware):
    - 'update_user' permission (for own profile)
    - 'update_any_user' permission (for any profile)
    
    Business logic:
    - Users can always update their own profile with 'update_user' permission
    - Updating other profiles requires the 'update_any_user' permission
    """
    return controller.update_user(user_id, user_update)

@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(
    user_id: int,
    request: Request,
    controller: UserController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
) -> dict:
    """
    Endpoint to delete a user.
    
    Permission requirements (handled by middleware):
    - 'delete_user' permission
    
    Business logic:
    - Admins with 'delete_user' permission can delete any user
    - Regular users cannot delete accounts (including their own)
    """
    return controller.delete_user(user_id)
