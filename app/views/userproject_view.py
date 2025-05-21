from fastapi import APIRouter, Depends, Path, Query
from app.controllers.userproject_controller import UserProjectController
from app.models.dtos.user_dtos import UserResponse
from app.models.dtos.project_dtos import ProjectResponse
from app.auth import auth_service
from typing import List

router = APIRouter(
    prefix="/project-users",
    tags=["User Projects"],
)

@router.post("/", status_code=201)
async def assign_user_to_project(
    user_id: int = Query(...,gt=0, description="ID of the user to assign"),
    project_id: int = Query(...,gt=0, description="ID of the project"),
    controller: UserProjectController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Assign a user to a project.
    """
    return controller.add_user(user_id, project_id)

@router.delete("/", status_code=200)
async def remove_user_from_project(
    user_id: int = Query(...,gt=0, description="ID of the user to remove"),
    project_id: int = Query(...,gt=0, description="ID of the project"),
    controller: UserProjectController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Remove a user from a project.
    """
    return controller.remove_user(user_id, project_id)

@router.get("/{project_id}/users", response_model=List[UserResponse])
async def get_users_for_project(
    project_id: int = Path(..., gt=0, description="Project ID (must be positive)"),
    controller: UserProjectController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    List all users assigned to a project with full user details.
    """
    return controller.get_users(project_id)

@router.get("/users/{user_id}/projects", response_model=List[ProjectResponse])
async def get_projects_for_user(
    user_id: int = Path(..., gt=0, description="User ID (must be positive)"),
    controller: UserProjectController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    List all projects assigned to a user with full project details.
    """
    return controller.get_projects(user_id)

@router.get("/me/projects", response_model=List[ProjectResponse])
async def get_my_projects(
    user_data: dict = Depends(auth_service.verify_user),
    controller: UserProjectController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get all projects assigned to the authenticated user.
    """
    user_id = user_data.get("user_id")
    return controller.get_projects(user_id)
