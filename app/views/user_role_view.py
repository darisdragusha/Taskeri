from fastapi import APIRouter, Depends, Request, HTTPException, status
from controllers import UserController
from typing import Dict, List
from models.dtos import UserResponse

router = APIRouter(prefix="/user-roles", tags=["User Roles"])

@router.post("/{user_id}/roles/{role_id}", response_model=Dict[str, str])
async def assign_role_to_user(
    user_id: int,
    role_id: int,
    request: Request,
    controller: UserController = Depends()
):
    """
    Assign a role to a user.
    
    Permission requirements (handled by middleware):
    - 'manage_user_roles' permission
    
    Business logic:
    - Only administrators or managers can assign roles
    - The target user must exist in the system
    - The role must exist in the system
    - Some role assignments may be restricted based on company policy
    """
    # Additional business logic could be added here if needed
    # For example, preventing regular users from being assigned admin roles
    requesting_user_id = request.state.user_id
    
    return controller.assign_role_to_user(user_id, role_id)

@router.delete("/{user_id}/roles/{role_id}", response_model=Dict[str, str])
async def remove_role_from_user(
    user_id: int,
    role_id: int,
    request: Request,
    controller: UserController = Depends()
):
    """
    Remove a role from a user.
    
    Permission requirements (handled by middleware):
    - 'manage_user_roles' permission
    
    Business logic:
    - Only administrators or managers can remove roles
    - Users should maintain at least one role in the system
    - System-critical role removals may be restricted
    - Users cannot remove their own admin role (prevents admin lockout)
    """
    return controller.remove_role_from_user(user_id, role_id)

@router.get("/{user_id}/roles", response_model=List[Dict[str, str]])
async def get_user_roles(
    user_id: int,
    request: Request,
    controller: UserController = Depends()
):
    """
    Get all roles assigned to a user.
    
    Permission requirements (handled by middleware):
    - 'manage_user_roles' permission
    
    Business logic:
    - Administrators and managers can view any user's roles
    - Users might be allowed to view their own roles (check middleware settings)
    """
    
    return controller.get_user_roles(user_id)