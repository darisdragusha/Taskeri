from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from controllers.role_permission_controller import RolePermissionController
from models.dtos.role_permission_dto import RolePermissionCreate, RolePermissionResponse
from utils import get_db
from typing import List
from auth import auth_service

router = APIRouter(prefix="/role-permissions", tags=["Role-Permissions"])

def get_role_permission_controller(db: Session = Depends(get_db)) -> RolePermissionController:
    return RolePermissionController(db)

@router.post("/", response_model=RolePermissionResponse)
def create_role_permission(
    data: RolePermissionCreate,
    request: Request,
    db: Session = Depends(get_db),
    controller: RolePermissionController = Depends(get_role_permission_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Assign a permission to a role.

    Business logic:
    - Prevent duplicate role-permission mappings (not handled here, assumed unique)
    - Ensure role and permission IDs exist (handled via foreign key constraints)
    """
    return controller.create_mapping(data)

@router.get("/", response_model=List[RolePermissionResponse])
def get_all_role_permissions(
    request: Request,
    db: Session = Depends(get_db),
    controller: RolePermissionController = Depends(get_role_permission_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Retrieve all role-permission mappings.
    """
    return controller.get_all_mappings()

@router.delete("/", response_model=dict)
def delete_role_permission(
    role_id: int,
    permission_id: int,
    request: Request,
    db: Session = Depends(get_db),
    controller: RolePermissionController = Depends(get_role_permission_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Remove a permission from a role.

    Business logic:
    - Mapping must exist or 404 is returned
    """
    success = controller.delete_mapping(role_id, permission_id)
    if not success:
        raise HTTPException(status_code=404, detail="Mapping not found")
    return {"detail": "Mapping deleted"}
