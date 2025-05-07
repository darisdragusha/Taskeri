from fastapi import APIRouter, Depends, status, Query, Body, Path, HTTPException, Request
from controllers import TaskController
from models.dtos import (
    TaskCreate, TaskUpdate, TaskResponse, TaskDetailResponse, 
    TaskListResponse, TaskFilterParams, TaskStatistics
)
from typing import List, Dict, Optional
from auth import auth_service
from datetime import date
from utils.permission_utils import PermissionChecker

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate, 
    controller: TaskController = Depends(), 
    user_data: dict = Depends(PermissionChecker.require_permission("create_task"))
):
    """
    Create a new task.
    
    Requires 'create_task' permission.
    """
    return controller.create_task(task_data)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int, 
    controller: TaskController = Depends(), 
    user_data: dict = Depends(PermissionChecker.check_resource_ownership("task", "task_id"))
):
    """
    Get a specific task by ID.
    
    Requires either:
    - Ownership of the task
    - Assignment to the task
    - Admin/Manager role
    """
    return controller.get_task(task_id)

@router.get("/{task_id}/details", response_model=TaskDetailResponse)
async def get_task_details(
    task_id: int, 
    controller: TaskController = Depends(), 
    user_data: dict = Depends(PermissionChecker.check_resource_ownership("task", "task_id"))
):
    """
    Get detailed information about a task including relationships.
    
    Requires either:
    - Ownership of the task
    - Assignment to the task
    - Admin/Manager role
    """
    return controller.get_task_details(task_id)

@router.get("/project/{project_id}", response_model=List[TaskResponse])
async def get_tasks_by_project(
    project_id: int, 
    controller: TaskController = Depends(), 
    user_data: dict = Depends(PermissionChecker.check_resource_ownership("project", "project_id"))
):
    """
    Get all tasks in a specific project.
    
    Requires either:
    - Admin/Manager role for the project
    """
    return controller.get_tasks_by_project(project_id)

@router.get("/user/{user_id}", response_model=List[TaskResponse])
async def get_tasks_by_user(
    user_id: int, 
    request: Request,
    controller: TaskController = Depends(), 
    user_data: dict = Depends(PermissionChecker.require_permissions(
        ["read_task", "read_any_user_task"], require_all=False
    ))
) -> List[TaskResponse]:
    """
    Get all tasks assigned to a specific user.
    
    Requires either:
    - 'read_task' permission (for own tasks)
    - 'read_any_user_task' permission (for anyone's tasks)
    """
    # Extra check to ensure a regular user can only access their own tasks
    requesting_user_id = user_data.get("user_id")
    if requesting_user_id != user_id:
        # Check if they have permission to view others' tasks
        has_permission = await PermissionChecker.check_permission(
            "read_any_user_task", 
            request.state.db, 
            requesting_user_id
        )
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own tasks"
            )
            
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
    user_data: dict = Depends(PermissionChecker.require_permission("read_task"))
):
    """
    Get paginated list of tasks with optional filtering.
    
    Requires 'read_task' permission.
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
    user_data: dict = Depends(PermissionChecker.require_permissions(
        ["update_task", "update_any_task"], require_all=False
    )),
    # The resource ownership check is now handled as a dependency for consistency.
):
    """
    Update a task's information.
    
    Requires either:
    - 'update_task' permission (for own tasks)
    - 'update_any_task' permission (for any task)
    """
    # The resource ownership check is now handled as a dependency for consistency.
        
    return controller.update_task(task_id, task_data)

@router.delete("/{task_id}", response_model=Dict[str, str])
async def delete_task(
    task_id: int, 
    request: Request,
    controller: TaskController = Depends(), 
    user_data: dict = Depends(PermissionChecker.require_permissions(
        ["delete_own_task", "delete_any_task"], require_all=False
    ))
):
    """
    Delete a task.
    
    Requires either:
    - 'delete_own_task' permission (for own tasks)
    - 'delete_any_task' permission (for any task)
    """
    # Similar to update, we need to check ownership if they don't have delete_any_task
    user_id = user_data.get("user_id")
    has_delete_any = await PermissionChecker.check_permission(
        "delete_any_task", 
        request.state.db, 
        user_id
    )
    
    if not has_delete_any:
        # Check if they are owner/assignee
        ownership_check = PermissionChecker.check_resource_ownership("task", "task_id")
        await ownership_check(request, user_data)
        
    return controller.delete_task(task_id)

@router.get("/statistics", response_model=TaskStatistics)
async def get_task_statistics(
    controller: TaskController = Depends(), 
    user_data: dict = Depends(PermissionChecker.require_permission("view_statistics"))
):
    """
    Get task statistics across the system.
    
    Requires 'view_statistics' permission.
    """
    return controller.get_task_statistics()