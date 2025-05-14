from fastapi import APIRouter, Depends, status, Query, Path, HTTPException, Request
from controllers import TaskController
from models.dtos import (
    TaskCreate, TaskUpdate, TaskResponse, TaskDetailResponse, 
    TaskListResponse, TaskFilterParams, TaskStatistics
)
from typing import List, Dict, Optional
from datetime import date
from auth import auth_service

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate, 
    controller: TaskController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Create a new task.
    
    Permission requirements (handled by middleware):
    - 'create_task' permission
    """
    return controller.create_task(task_data)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int, 
    controller: TaskController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get a specific task by ID.
    
    Permission requirements (handled by middleware):
    - 'read_task' permission (for tasks assigned to the user)
    - 'read_any_task' permission (for any task)
    
    Business logic:
    - Users can access tasks they are assigned to
    - Users with 'read_any_task' can access any task
    - Admins/Managers can access any task
    """
    return controller.get_task(task_id)

@router.get("/{task_id}/details", response_model=TaskDetailResponse)
async def get_task_details(
    task_id: int, 
    controller: TaskController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get detailed information about a task including relationships.
    
    Permission requirements (handled by middleware):
    - 'read_task' permission (for tasks assigned to the user)
    - 'read_any_task' permission (for any task)
    
    Business logic:
    - Users can access details of tasks they are assigned to
    - Users with 'read_any_task' can access details of any task
    - Admins/Managers can access details of any task
    """
    return controller.get_task_details(task_id)

@router.get("/project/{project_id}", response_model=List[TaskResponse])
async def get_tasks_by_project(
    project_id: int, 
    controller: TaskController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get all tasks in a specific project.
    
    Permission requirements (handled by middleware):
    - 'read_task' permission
    
    Business logic:
    - Users can view tasks for projects they're involved with
    - Admins/Managers can view all project tasks
    """
    return controller.get_tasks_by_project(project_id)

@router.get("/user/{user_id}", response_model=List[TaskResponse])
async def get_tasks_by_user(
    user_id: int, 
    request: Request,
    controller: TaskController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
) -> List[TaskResponse]:
    """
    Get all tasks assigned to a specific user.
    
    Permission requirements (handled by middleware):
    - 'read_task' permission (for own tasks)
    - 'read_any_user_task' permission (for others' tasks)
    
    Business logic:
    - Users can always view their own tasks
    - Viewing others' tasks requires the 'read_any_user_task' permission
    """
            
    return controller.get_tasks_by_user(user_id)

@router.get("/", response_model=TaskListResponse)
async def get_tasks_paginated(
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    page_size: int = Query(20, ge=1, le=100, description="Number of items per page"),
    status: Optional[List[str]] = Query(None, description="Filter by status values"),
    priority: Optional[List[str]] = Query(None, description="Filter by priority values"),
    due_date_from: Optional[date] = Query(None, description="Filter by due date (from)"),
    due_date_to: Optional[date] = Query(None, description="Filter by due date (to)"),
    assigned_to_user_id: Optional[int] = Query(None, description="Filter by assigned user"),
    project_id: Optional[int] = Query(None, description="Filter by project"),
    search_term: Optional[str] = Query(None, description="Search in task name and description"),
    controller: TaskController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get paginated list of tasks with optional filtering.
    
    Permission requirements (handled by middleware):
    - 'read_task' permission
    
    Business logic:
    - Results will be filtered based on user permissions
    - Regular users see only their assigned tasks
    - Admins/Managers see all tasks
    """
    filter_params = TaskFilterParams(
        status=status, 
        priority=priority,
        due_date_from=due_date_from,
        due_date_to=due_date_to,
        assigned_to_user_id=assigned_to_user_id,
        project_id=project_id,
        search_term=search_term
    )
    return controller.get_tasks_paginated(page, page_size, filter_params)

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int, 
    task_data: TaskUpdate, 
    controller: TaskController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Update a task's information.
    
    Permission requirements (handled by middleware):
    - 'update_task' permission (for tasks assigned to the user)
    - 'update_any_task' permission (for any task)
    
    Business logic:
    - Users can update tasks they are assigned to
    - Users with 'update_any_task' can update any task
    - Admins/Managers can update any task
    """
    return controller.update_task(task_id, task_data)

@router.delete("/{task_id}", response_model=Dict[str, str])
async def delete_task(
    task_id: int, 
    controller: TaskController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Delete a task.
    
    Permission requirements (handled by middleware):
    - 'delete_own_task' permission (for tasks created by the user)
    - 'delete_any_task' permission (for any task)
    
    Business logic:
    - Users can only delete their own tasks if they have 'delete_own_task' permission
    - Users with 'delete_any_task' permission can delete any task
    - Admins can delete any task
    """
    return controller.delete_task(task_id)

@router.get("/statistics", response_model=TaskStatistics)
async def get_task_statistics(
    controller: TaskController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get task statistics across the system.
    
    Permission requirements (handled by middleware):
    - 'view_statistics' permission
    
    Business logic:
    - Only users with explicit statistics viewing permission can access this endpoint
    - Typically limited to managers and administrators
    """
    return controller.get_task_statistics()