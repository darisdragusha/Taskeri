from fastapi import APIRouter, Depends, Path, Query
from controllers.userproject_controller import UserProjectController
from models.dtos.user_dtos import UserResponse
from typing import List

router = APIRouter(
    prefix="/project-users",
    tags=["project-users"],
)

@router.post("/", status_code=201)
async def assign_user_to_project(
    user_id: int = Query(...,gt=0, description="ID of the user to assign"),
    project_id: int = Query(...,gt=0, description="ID of the project"),
    controller: UserProjectController = Depends()
):
    """
    Assign a user to a project.
    """
    return controller.add_user(user_id, project_id)

@router.delete("/", status_code=200)
async def remove_user_from_project(
    user_id: int = Query(...,gt=0, description="ID of the user to remove"),
    project_id: int = Query(...,gt=0, description="ID of the project"),
    controller: UserProjectController = Depends()
):
    """
    Remove a user from a project.
    """
    return controller.remove_user(user_id, project_id)

@router.get("/{project_id}/users", response_model=List[UserResponse])
async def get_users_for_project(
    project_id: int = Path(..., gt=0, description="Project ID (must be positive)"),
    controller: UserProjectController = Depends()
):
    """
    List all users assigned to a project with full user details.
    """
    return controller.get_users(project_id)
