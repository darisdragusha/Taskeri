from fastapi import APIRouter, Depends, status, Query, Path, HTTPException
from controllers.project_controller import ProjectController
from models.dtos.project_dtos import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectStatistics
from typing import List, Dict
from auth import auth_service

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    controller: ProjectController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Create a new project (optionally assign users).

    Permission requirements (handled by middleware):
    - 'create_project' permission

    Business logic:
    - Only authorized users (e.g., Admins/PMs) can create projects
    - Optional user assignments can be included at creation
    """
    return controller.create_project(project_data)

@router.get("/", response_model=List[ProjectResponse])
async def get_all_projects(
    controller: ProjectController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Retrieve all projects in the system.

    Permission requirements (handled by middleware):
    - 'read_projects' permission

    Business logic:
    - Users with access can see the full list of projects
    """
    return controller.get_all_projects()

@router.get("/statistics", response_model=ProjectStatistics)
async def get_project_statistics(
    controller: ProjectController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Retrieve statistics about project statuses.

    Permission requirements (handled by middleware):
    - 'view_statistics' permission

    Business logic:
    - Useful for admins and managers to monitor project distribution
    """
    return controller.get_project_statistics()

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project_by_id(
    project_id: int = Path(..., description="ID of the project to retrieve"),
    controller: ProjectController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Retrieve a single project by its ID.

    Permission requirements (handled by middleware):
    - 'read_project' permission

    Business logic:
    - Users can view projects they’re assigned to
    - Admins/Managers can view all projects
    """
    return controller.get_project(project_id)

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    controller: ProjectController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Update an existing project (optionally reassign users).

    Permission requirements (handled by middleware):
    - 'update_project' permission (if the user created it)
    - 'update_any_project' permission (for full access)

    Business logic:
    - Users with correct permission can update any field
    - User assignments can be replaced if provided
    """
    return controller.update_project(project_id, project_update)

@router.delete("/{project_id}", response_model=Dict[str, str])
async def delete_project(
    project_id: int,
    controller: ProjectController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Delete a project by ID.

    Permission requirements (handled by middleware):
    - 'delete_project' or 'delete_any_project' permission

    Business logic:
    - Project deletion should be restricted to admins or project creators
    """
    return controller.delete_project(project_id)
