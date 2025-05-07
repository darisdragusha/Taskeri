# app/views/permission_view.py
from fastapi import APIRouter, Depends
from controllers import PermissionController
from models.dtos.permission_dtos import PermissionCreate, PermissionUpdate, PermissionResponse
from typing import List
from auth import auth_service

router = APIRouter()

@router.post("/permissions", response_model=PermissionResponse)
async def create_permission(
    permission_create: PermissionCreate,
    controller: PermissionController = Depends(),
    user_data: dict = Depends(auth_service.verify_user)
) -> PermissionResponse:
    """
    Endpoint to create a new permission.
    """
    return controller.create_permission(permission_create)

@router.get("/permissions/{permission_id}", response_model=PermissionResponse)
async def get_permission(
    permission_id: int,
    controller: PermissionController = Depends(),
    user_data: dict = Depends(auth_service.verify_user)
) -> PermissionResponse:
    """
    Endpoint to get a permission by ID.
    """
    return controller.get_permission(permission_id)

@router.put("/permissions/{permission_id}", response_model=PermissionResponse)
async def update_permission(
    permission_id: int,
    permission_update: PermissionUpdate,
    controller: PermissionController = Depends(),
    user_data: dict = Depends(auth_service.verify_user)
) -> PermissionResponse:
    """
    Endpoint to update a permission.
    """
    return controller.update_permission(permission_id, permission_update)

@router.delete("/permissions/{permission_id}", response_model=dict)
async def delete_permission(
    permission_id: int,
    controller: PermissionController = Depends(),
    user_data: dict = Depends(auth_service.verify_user)
) -> dict:
    """
    Endpoint to delete a permission.
    """
    return controller.delete_permission(permission_id)

@router.get("/permissions", response_model=List[PermissionResponse])
async def get_all_permissions(
    controller: PermissionController = Depends(),
    user_data: dict = Depends(auth_service.verify_user)
) -> List[PermissionResponse]:
    """
    Endpoint to retrieve all permissions.
    """
    return controller.get_all_permissions()