from fastapi import APIRouter, Depends, status, Query, Body, Path
from controllers.task_controller import TaskController
from models.dtos.task_dtos import (
    TaskCreate, TaskUpdate, TaskResponse, TaskDetailResponse, 
    TaskListResponse, TaskFilterParams, TaskStatistics
)
from typing import List, Dict, Optional
from auth import auth_service
from datetime import date

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreate, controller: TaskController = Depends(), user=Depends(auth_service.verify_user)):
    """
    Create a new task.
    
    Requires authentication.
    """
    return controller.create_task(task_data)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, controller: TaskController = Depends(), user=Depends(auth_service.verify_user)):
    """
    Get a specific task by ID.
    
    Requires authentication.
    """
    return controller.get_task(task_id)

@router.get("/{task_id}/details", response_model=TaskDetailResponse)
async def get_task_details(task_id: int, controller: TaskController = Depends(), user=Depends(auth_service.verify_user)):
    """
    Get detailed information about a task including relationships.
    
    Requires authentication.
    """
    return controller.get_task_details(task_id)

@router.get("/project/{project_id}", response_model=List[TaskResponse])
async def get_tasks_by_project(project_id: int, controller: TaskController = Depends(), user=Depends(auth_service.verify_user)):
    """
    Get all tasks in a specific project.
    
    Requires authentication.
    """
    return controller.get_tasks_by_project(project_id)

@router.get("/user/{user_id}", response_model=List[TaskResponse])
async def get_tasks_by_user(user_id: int, controller: TaskController = Depends(), user=Depends(auth_service.verify_user)):
    """
    Get all tasks assigned to a specific user.
    
    Requires authentication.
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
    user=Depends(auth_service.verify_user)
):
    """
    Get paginated list of tasks with optional filtering.
    
    Requires authentication.
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
async def update_task(task_id: int, task_data: TaskUpdate, controller: TaskController = Depends(), user=Depends(auth_service.verify_user)):
    """
    Update a task's information.
    
    Requires authentication.
    """
    return controller.update_task(task_id, task_data)

@router.delete("/{task_id}", response_model=Dict[str, str])
async def delete_task(task_id: int, controller: TaskController = Depends(), user=Depends(auth_service.verify_user)):
    """
    Delete a task.
    
    Requires authentication.
    """
    return controller.delete_task(task_id)

@router.get("/statistics", response_model=TaskStatistics)
async def get_task_statistics(controller: TaskController = Depends(), user=Depends(auth_service.verify_user)):
    """
    Get task statistics across the system.
    
    Requires authentication.
    """
    return controller.get_task_statistics()