# app/views/permission_view.py
from fastapi import APIRouter, Depends, Request
from controllers import PermissionController
from models.dtos import PermissionCreate, PermissionUpdate, PermissionResponse
from typing import List
from utils.permission_utils import PermissionChecker

router = APIRouter()

@router.post("/permissions", response_model=PermissionResponse)
async def create_permission(
    permission_create: PermissionCreate,
    request: Request,
    controller: PermissionController = Depends(),
    user_data: dict = Depends(PermissionChecker.require_permission("create_permission"))
) -> PermissionResponse:
    """
    Endpoint to create a new permission.
    Requires the 'create_permission' permission.
    """
    return controller.create_permission(permission_create)

@router.get("/permissions/{permission_id}", response_model=PermissionResponse)
async def get_permission(
    permission_id: int,
    request: Request,
    controller: PermissionController = Depends(),
    user_data: dict = Depends(PermissionChecker.require_permission("read_permission"))
) -> PermissionResponse:
    """
    Endpoint to get a permission by ID.
    Requires the 'read_permission' permission.
    """
    return controller.get_permission(permission_id)

@router.put("/permissions/{permission_id}", response_model=PermissionResponse)
async def update_permission(
    permission_id: int,
    permission_update: PermissionUpdate,
    request: Request,
    controller: PermissionController = Depends(),
    user_data: dict = Depends(PermissionChecker.require_permission("update_permission"))
) -> PermissionResponse:
    """
    Endpoint to update a permission.
    Requires the 'update_permission' permission.
    """
    return controller.update_permission(permission_id, permission_update)

@router.delete("/permissions/{permission_id}", response_model=dict)
async def delete_permission(
    permission_id: int,
    request: Request,
    controller: PermissionController = Depends(),
    user_data: dict = Depends(PermissionChecker.require_permission("delete_permission"))
) -> dict:
    """
    Endpoint to delete a permission.
    Requires the 'delete_permission' permission.
    """
    return controller.delete_permission(permission_id)

@router.get("/permissions", response_model=List[PermissionResponse])
async def get_all_permissions(
    request: Request,
    controller: PermissionController = Depends(),
    user_data: dict = Depends(PermissionChecker.require_permission("read_permission"))
) -> List[PermissionResponse]:
    """
    Endpoint to retrieve all permissions.
    Requires the 'read_permission' permission.
    """
    return controller.get_all_permissions()