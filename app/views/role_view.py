# app/views/role_view.py
from fastapi import APIRouter, Depends
from controllers.role_controller import RoleController
from typing import List
from models.dtos.role_dtos import RoleCreate, RoleUpdate, RoleResponse
from auth import auth_service

router = APIRouter()

@router.post("/roles", response_model=RoleResponse)
async def create_role(
    role_create: RoleCreate,
    controller: RoleController = Depends(),
    user_data: dict = Depends(auth_service.verify_user)
) -> RoleResponse:
    """
    Endpoint to create a new role.
    """
    return controller.create_role(role_create)

@router.get("/roles/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int,
    controller: RoleController = Depends(),
    user_data: dict = Depends(auth_service.verify_user)
) -> RoleResponse:
    """
    Endpoint to get a role by ID.
    """
    return controller.get_role(role_id)

@router.put("/roles/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_update: RoleUpdate,
    controller: RoleController = Depends(),
    user_data: dict = Depends(auth_service.verify_user)
) -> RoleResponse:
    """
    Endpoint to update a role.
    """
    return controller.update_role(role_id, role_update)

@router.delete("/roles/{role_id}", response_model=dict)
async def delete_role(
    role_id: int,
    controller: RoleController = Depends(),
    user_data: dict = Depends(auth_service.verify_user)
) -> dict:
    """
    Endpoint to delete a role.
    """
    return controller.delete_role(role_id)

@router.get("/roles", response_model=List[RoleResponse])
async def get_all_roles(
    controller: RoleController = Depends(),
    user_data: dict = Depends(auth_service.verify_user)
) -> List[RoleResponse]:
    """
    Endpoint to retrieve all roles.
    """
    return controller.get_all_roles()