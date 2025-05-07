# app/views/user_view.py
from fastapi import HTTPException, status, APIRouter, Depends, Request
from controllers import UserController
from models.dtos import UserCreate, UserUpdate, UserResponse
from auth import auth_service
from utils.permission_utils import PermissionChecker

router = APIRouter()

@router.post("/users", response_model=UserResponse)
async def create_user(
    user_create: UserCreate,
    controller: UserController = Depends(),
    user_data: dict = Depends(PermissionChecker.require_permission("create_user"))
) -> UserResponse:
    """
    Endpoint to create a new user.
    Requires the 'create_user' permission.
    """
    return controller.create_user(user_create)

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    request: Request,
    controller: UserController = Depends(),
    user_data: dict = Depends(PermissionChecker.require_permissions(
        ["read_user", "read_any_user"], require_all=False
    ))
) -> UserResponse:
    """
    Endpoint to get a user by ID.
    Requires either:
    - 'read_user' permission (for own profile)
    - 'read_any_user' permission (for any profile)
    """
    # Check if user is requesting their own profile or has permission to view any user
    requesting_user_id = user_data.get("user_id")
    if requesting_user_id != user_id:
        # If not their own profile, check if they have read_any_user permission
        has_permission = await PermissionChecker.check_permission(
            "read_any_user", 
            request.state.db, 
            requesting_user_id
        )
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own profile"
            )
    
    return controller.get_user(user_id)

@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    request: Request,
    controller: UserController = Depends(),
    user_data: dict = Depends(PermissionChecker.require_permissions(
        ["update_user", "update_any_user"], require_all=False
    ))
) -> UserResponse:
    """
    Endpoint to update a user.
    Requires either:
    - 'update_user' permission (for own profile)
    - 'update_any_user' permission (for any profile)
    """
    # Check if user is updating their own profile or has permission to update any user
    requesting_user_id = user_data.get("user_id")
    if requesting_user_id != user_id:
        # If not their own profile, check if they have update_any_user permission
        has_permission = await PermissionChecker.check_permission(
            "update_any_user", 
            request.state.db, 
            requesting_user_id
        )
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only update your own profile"
            )
    
    return controller.update_user(user_id, user_update)

@router.delete("/users/{user_id}", response_model=dict)
async def delete_user(
    user_id: int,
    controller: UserController = Depends(),
    user_data: dict = Depends(PermissionChecker.require_permission("delete_user"))
) -> dict:
    """
    Endpoint to delete a user.
    Requires the 'delete_user' permission.
    """
    return controller.delete_user(user_id)
