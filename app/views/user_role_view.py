from fastapi import APIRouter, Depends, HTTPException, status, Request
from controllers import UserController
from typing import Dict, List
from utils.permission_utils import PermissionChecker
from models.dtos import UserResponse

router = APIRouter(prefix="/user-roles", tags=["User Roles"])

@router.post("/{user_id}/roles/{role_id}", response_model=Dict[str, str])
async def assign_role_to_user(
    user_id: int,
    role_id: int,
    request: Request,
    controller: UserController = Depends(),
    user_data: dict = Depends(PermissionChecker.require_permission("manage_user_roles"))
):
    """
    Assign a role to a user.
    
    Requires 'manage_user_roles' permission.
    """
    return controller.assign_role_to_user(user_id, role_id)

@router.delete("/{user_id}/roles/{role_id}", response_model=Dict[str, str])
async def remove_role_from_user(
    user_id: int,
    role_id: int,
    request: Request,
    controller: UserController = Depends(),
    user_data: dict = Depends(PermissionChecker.require_permission("manage_user_roles"))
):
    """
    Remove a role from a user.
    
    Requires 'manage_user_roles' permission.
    """
    return controller.remove_role_from_user(user_id, role_id)

@router.get("/{user_id}/roles", response_model=List[Dict[str, str]])
async def get_user_roles(
    user_id: int,
    request: Request,
    controller: UserController = Depends(),
    user_data: dict = Depends(PermissionChecker.require_permission("manage_user_roles"))
):
    """
    Get all roles assigned to a user.
    
    Requires 'manage_user_roles' permission.
    """
    return controller.get_user_roles(user_id)