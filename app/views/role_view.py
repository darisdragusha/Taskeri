# app/views/role_view.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from app.controllers import RoleController
from typing import List
from app.models.dtos import RoleCreate, RoleUpdate, RoleResponse
from app.utils import get_db 
from app.auth import auth_service


router = APIRouter(prefix="/roles",tags=["Roles"])

@router.post("", response_model=RoleResponse)
async def create_role(
    role_create: RoleCreate,
    request: Request,
    controller: RoleController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
) -> RoleResponse:
    """
    Endpoint to create a new role.
    
    Permission requirements (handled by middleware):
    - 'create_role' permission
    
    Business logic:
    - Only administrators should be able to create new roles
    - Role names should be unique in the system
    """
    return controller.create_role(role_create)

@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int,
    request: Request,
    controller: RoleController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
) -> RoleResponse:
    """
    Endpoint to get a role by ID.
    
    Permission requirements (handled by middleware):
    - 'read_role' permission
    
    Business logic:
    - All authenticated users with permission can view role details
    """
    return controller.get_role(role_id)

@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_update: RoleUpdate,
    request: Request,
    controller: RoleController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
) -> RoleResponse:
    """
    Endpoint to update a role.
    
    Permission requirements (handled by middleware):
    - 'update_role' permission
    
    Business logic:
    - Only administrators should be able to modify existing roles
    - System-critical roles (Admin, Manager, Employee) may have additional protection
    """
    return controller.update_role(role_id, role_update)

@router.delete("/{role_id}", response_model=dict)
async def delete_role(
    role_id: int,
    request: Request,
    controller: RoleController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
) -> dict:
    """
    Endpoint to delete a role.
    
    Permission requirements (handled by middleware):
    - 'delete_role' permission
    
    Business logic:
    - Only administrators should be able to delete roles
    - System-critical roles (Admin, Manager, Employee) cannot be deleted
    - Roles currently assigned to users should be protected or reassigned
    """
    return controller.delete_role(role_id)

@router.get("", response_model=List[RoleResponse])
async def get_all_roles(
    request: Request,
    controller: RoleController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
) -> List[RoleResponse]:
    """
    Endpoint to retrieve all roles.
    
    Permission requirements (handled by middleware):
    - 'read_role' permission
    
    Business logic:
    - All authenticated users with permission can view all roles
    """
    return controller.get_all_roles()