# app/views/role_view.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from controllers import RoleController
from typing import List
from models.dtos import RoleCreate, RoleUpdate, RoleResponse
from utils.permission_utils import PermissionChecker

router = APIRouter()

@router.post("/roles", response_model=RoleResponse)
async def create_role(
    role_create: RoleCreate,
    request: Request,
    controller: RoleController = Depends(),
    user_data: dict = Depends(PermissionChecker.require_permission("create_role"))
) -> RoleResponse:
    """
    Endpoint to create a new role.
    Requires the 'create_role' permission.
    """
    return controller.create_role(role_create)

@router.get("/roles/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int,
    request: Request,
    controller: RoleController = Depends(),
    user_data: dict = Depends(PermissionChecker.require_permission("read_role"))
) -> RoleResponse:
    """
    Endpoint to get a role by ID.
    Requires the 'read_role' permission.
    """
    return controller.get_role(role_id)

@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_update: RoleUpdate,
    request: Request,
    controller: RoleController = Depends(),
    user_data: dict = Depends(PermissionChecker.require_permission("update_role"))
) -> RoleResponse:
    """
    Endpoint to update a role.
    Requires the 'update_role' permission.
    """
    return controller.update_role(role_id, role_update)

@router.delete("/roles/{role_id}", response_model=dict)
async def delete_role(
    role_id: int,
    request: Request,
    controller: RoleController = Depends(),
    user_data: dict = Depends(PermissionChecker.require_permission("delete_role"))
) -> dict:
    """
    Endpoint to delete a role.
    Requires the 'delete_role' permission.
    """
    return controller.delete_role(role_id)

@router.get("/roles", response_model=List[RoleResponse])
async def get_all_roles(
    request: Request,
    controller: RoleController = Depends(),
    user_data: dict = Depends(PermissionChecker.require_permission("read_role"))
) -> List[RoleResponse]:
    """
    Endpoint to retrieve all roles.
    Requires the 'read_role' permission.
    """
    return controller.get_all_roles()