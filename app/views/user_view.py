# app/views/user_view.py
from fastapi import APIRouter, Depends
from controllers import UserController
from models.dtos.user_dtos import UserCreate, UserUpdate, UserResponse
from auth import auth_service

router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def create_user(
    user_create: UserCreate,
    controller: UserController = Depends(),
    user_data: dict = Depends(auth_service.verify_user)
) -> UserResponse:
    """
    Endpoint to create a new user.
    """
    return controller.create_user(user_create)

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    controller: UserController = Depends(),
    user_data: dict = Depends(auth_service.verify_user)
) -> UserResponse:
    """
    Endpoint to get a user by ID.

    """
    return controller.get_user(user_id)

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    controller: UserController = Depends(),
    user_data: dict = Depends(auth_service.verify_user)
) -> UserResponse:
    """
    Endpoint to update a user.
    """
    return controller.update_user(user_id, user_update)

@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(
    user_id: int,
    controller: UserController = Depends(),
    user_data: dict = Depends(auth_service.verify_user)
) -> dict:
    """
    Endpoint to delete a user.
    """
    return controller.delete_user(user_id)
