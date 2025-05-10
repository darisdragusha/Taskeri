# app/views/permission_view.py
from fastapi import APIRouter, Depends, Request
from controllers import PermissionController
from models.dtos import PermissionCreate, PermissionUpdate, PermissionResponse
from typing import List

router = APIRouter()

@router.post("/permissions", response_model=PermissionResponse)
async def create_permission(
    permission_create: PermissionCreate,
    request: Request,
    controller: PermissionController = Depends()
) -> PermissionResponse:
    """
    Endpoint to create a new permission.
    
    Permission requirements (handled by middleware):
    - 'create_permission' permission
    
    Business logic:
    - Only administrators should be able to create new permissions
    - Permission names should be unique in the system
    - Permissions are the foundation of the security system
    """
    return controller.create_permission(permission_create)

@router.get("/permissions/{permission_id}", response_model=PermissionResponse)
async def get_permission(
    permission_id: int,
    request: Request,
    controller: PermissionController = Depends()
) -> PermissionResponse:
    """
    Endpoint to get a permission by ID.
    
    Permission requirements (handled by middleware):
    - 'read_permission' permission
    
    Business logic:
    - Users with specific permission can view permission details
    - Typically restricted to administrators and security managers
    """
    return controller.get_permission(permission_id)

@router.put("/permissions/{permission_id}", response_model=PermissionResponse)
async def update_permission(
    permission_id: int,
    permission_update: PermissionUpdate,
    request: Request,
    controller: PermissionController = Depends()
) -> PermissionResponse:
    """
    Endpoint to update a permission.
    
    Permission requirements (handled by middleware):
    - 'update_permission' permission
    
    Business logic:
    - Only administrators should be able to modify existing permissions
    - System-critical permissions should have additional protection
    - Changes to permissions can have system-wide security implications
    """
    return controller.update_permission(permission_id, permission_update)

@router.delete("/permissions/{permission_id}", response_model=dict)
async def delete_permission(
    permission_id: int,
    request: Request,
    controller: PermissionController = Depends()
) -> dict:
    """
    Endpoint to delete a permission.
    
    Permission requirements (handled by middleware):
    - 'delete_permission' permission
    
    Business logic:
    - Only administrators should be able to delete permissions
    - System-critical permissions cannot be deleted
    - Permissions currently assigned to roles should be protected
    - Deleting permissions can affect multiple roles and users
    """
    return controller.delete_permission(permission_id)

@router.get("/permissions", response_model=List[PermissionResponse])
async def get_all_permissions(
    request: Request,
    controller: PermissionController = Depends()
) -> List[PermissionResponse]:
    """
    Endpoint to retrieve all permissions.
    
    Permission requirements (handled by middleware):
    - 'read_permission' permission
    
    Business logic:
    - Users with specific permission can view all permissions
    - Typically restricted to administrators and security managers
    """
    return controller.get_all_permissions()