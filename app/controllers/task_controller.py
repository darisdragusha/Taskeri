from fastapi import HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.repositories import TaskRepository
from app.utils import get_db
from app.models.dtos import (
    TaskCreate, TaskUpdate, TaskResponse, TaskDetailResponse, 
    TaskListResponse, TaskFilterParams, TaskStatistics
)
from typing import List, Dict, Any, Optional
from datetime import date, datetime
import logging

logger = logging.getLogger(__name__)

class TaskController:
    """Controller class for handling task operations."""

    def __init__(self, db_session: Session = Depends(get_db)):
        """
        Initialize the TaskController.

        Args:
            db_session (Session): SQLAlchemy database session.
        """
        self.repository = TaskRepository(db_session)

    def create_task(self, task_create: TaskCreate) -> TaskResponse:
        """
        Create a new task.

        Args:
            task_create (TaskCreate): Data for the new task.

        Returns:
            TaskResponse: Created task response.
            
        Raises:
            HTTPException: If there's a validation error or database error.
        """
        try:
            task = self.repository.create_task(
                project_id=task_create.project_id,
                name=task_create.name,
                description=task_create.description,
                priority=task_create.priority.value if task_create.priority else "Medium",
                status=task_create.status.value if task_create.status else "To Do",
                due_date=task_create.due_date,
                assigned_user_ids=task_create.assigned_user_ids
            )
            
            
            assigned_users = None
            if task_create.assigned_user_ids:
                assigned_users = self.repository.get_task_assignments(task.id)
                
            response = TaskResponse.from_orm(task)
            response.assigned_users = assigned_users
            
            return response
            
        except SQLAlchemyError as e:
           
            # logger.error(f"Database error creating task: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
           
            # logger.error(f"Unexpected error creating task: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred"
            )

    def get_task(self, task_id: int) -> TaskResponse:
        """
        Get a task by ID.

        Args:
            task_id (int): Task ID.

        Returns:
            TaskResponse: Retrieved task response.
            
        Raises:
            HTTPException: If task not found or database error.
        """
        try:
            task = self.repository.get_task_by_id(task_id)
            if not task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )
                
            logger.debug("Task found")
            assigned_users = self.repository.get_task_assignments(task_id)
            logger.info(assigned_users)
            response = TaskResponse.model_validate(task)
            response.assigned_users = assigned_users
            
            return response
            
        except HTTPException:
            raise
        except SQLAlchemyError as e:
           
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
        except Exception as e:
           
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred"
            )
    
    def get_task_details(self, task_id: int) -> TaskDetailResponse:
        """
        Get detailed task information including relationships.
        
        Args:
            task_id (int): Task ID
            
        Returns:
            TaskDetailResponse: Detailed task response with related data
            
        Raises:
            HTTPException: If task not found or database error
        """
        try:
            task = self.repository.get_task_by_id(task_id)
            if not task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )
            
           
            task_details = self.repository.get_task_with_details(task_id)
            
            return task_details
            
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
            
    def get_tasks_by_project(self, project_id: int) -> List[TaskResponse]:
        """
        Get all tasks for a specific project.
        
        Args:
            project_id (int): Project ID
            
        Returns:
            List[TaskResponse]: List of tasks in the project
            
        Raises:
            HTTPException: If database error occurs
        """
        try:
            tasks = self.repository.get_tasks_by_project(project_id)
            return [TaskResponse.from_orm(task) for task in tasks]
        except SQLAlchemyError as e:
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
            
    def get_tasks_by_user(self, user_id: int) -> List[TaskResponse]:
        """
        Get all tasks assigned to a specific user.
        
        Args:
            user_id (int): User ID
            
        Returns:
            List[TaskResponse]: List of tasks assigned to the user
            
        Raises:
            HTTPException: If database error occurs
        """
        try:
            tasks = self.repository.get_tasks_by_user(user_id)
            return [TaskResponse.from_orm(task) for task in tasks]
        except SQLAlchemyError as e:
           
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
    
    def get_tasks_paginated(self, 
                          page: int = 1, 
                          page_size: int = 20,
                          filter_params: Optional[TaskFilterParams] = None) -> TaskListResponse:
        """
        Get paginated task list with optional filtering.
        
        Args:
            page (int): Page number (starting from 1)
            page_size (int): Number of items per page
            filter_params (TaskFilterParams): Filters to apply
            
        Returns:
            TaskListResponse: Paginated list of tasks
            
        Raises:
            HTTPException: If database error occurs
        """
        try:
            tasks, total = self.repository.get_tasks_paginated(
                page=page,
                page_size=page_size,
                status=filter_params.status if filter_params else None,
                priority=filter_params.priority if filter_params else None,
                due_date_from=filter_params.due_date_from if filter_params else None,
                due_date_to=filter_params.due_date_to if filter_params else None,
                assigned_to_user_id=filter_params.assigned_to_user_id if filter_params else None,
                project_id=filter_params.project_id if filter_params else None,
                search_term=filter_params.search_term if filter_params else None
            )
            
            return TaskListResponse(
                items=[TaskResponse.from_orm(task) for task in tasks],
                total=total,
                page=page,
                page_size=page_size
            )
            
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )

    def update_task(self, task_id: int, task_update: TaskUpdate) -> TaskResponse:
        """
        Update a task's information.

        Args:
            task_id (int): Task ID.
            task_update (TaskUpdate): Updated task data.

        Returns:
            TaskResponse: Updated task response.
            
        Raises:
            HTTPException: If task not found or database error.
        """
        try:
           
            update_data = task_update.dict(exclude={"assigned_user_ids"}, exclude_none=True)
            
           
            if "priority" in update_data and update_data["priority"]:
                update_data["priority"] = update_data["priority"].value
                
            if "status" in update_data and update_data["status"]:
                update_data["status"] = update_data["status"].value
            
            task = self.repository.update_task(
                task_id=task_id,
                update_data=update_data,
                assigned_user_ids=task_update.assigned_user_ids
            )
            
            if not task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )
                
            
            assigned_users = self.repository.get_task_assignments(task_id)
            
            response = TaskResponse.from_orm(task)
            response.assigned_users = assigned_users
            
            return response
            
        except HTTPException:
            raise
        except SQLAlchemyError as e:
           
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        except Exception as e:
           
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred"
            )

    def delete_task(self, task_id: int) -> Dict[str, str]:
        """
        Delete a task.

        Args:
            task_id (int): Task ID.

        Returns:
            dict: Success message.
            
        Raises:
            HTTPException: If task not found or database error.
        """
        try:
            task = self.repository.delete_task(task_id)
            if not task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Task not found"
                )
                
            return {"message": "Task deleted successfully"}
            
        except HTTPException:
            raise
        except SQLAlchemyError as e:
           
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
        except Exception as e:
           
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred"
            )
    
    def get_task_statistics(self) -> TaskStatistics:
        """
        Get task statistics across the system.
        
        Returns:
            TaskStatistics: Task statistics response
            
        Raises:
            HTTPException: If database error occurs
        """
        try:
            stats = self.repository.get_task_statistics()
            return stats
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )