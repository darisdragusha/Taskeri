from sqlalchemy.orm import Session, joinedload
from sqlalchemy import update, func, or_, and_, desc, text, case
from typing import Optional, List, Dict, Any, Tuple
from app.models.task import Task
from app.models.task_assignment import TaskAssignment
from app.models.comment import Comment
from app.models.file_attachment import FileAttachment
from app.models.user import User
from app.models.project import Project
from app.models.dtos import TaskDetailResponse, TaskStatistics, StatusEnum, TaskResponse
from app.models.dtos.notification_dtos import NotificationCreate
from datetime import date, datetime
import logging
from app.controllers.notification_controller import NotificationController

class TaskRepository:
    """Repository class for handling task-related database operations."""

    def __init__(self, db_session: Session):
        """
        Initialize the TaskRepository.

        Args:
            db_session (Session): SQLAlchemy database session.
        """
        self.db_session = db_session

    def create_task(self, 
                   project_id: int, 
                   name: str, 
                   description: Optional[str] = None,
                   priority: str = "Medium",
                   status: str = "To Do",
                   due_date: Optional[date] = None,
                   assigned_user_ids: Optional[List[int]] = None) -> Task:
        """
        Create a new task.

        Args:
            project_id (int): ID of the project this task belongs to
            name (str): Task name
            description (Optional[str]): Task description
            priority (str): Task priority (Low, Medium, High)
            status (str): Task status (To Do, In Progress, etc.)
            due_date (Optional[date]): Task due date
            assigned_user_ids (Optional[List[int]]): List of user IDs to assign to this task

        Returns:
            Task: The newly created task object
        """
        try:
            # Create the task
            task = Task(
                project_id=project_id,
                name=name,
                description=description,
                priority=priority,
                status=status,
                due_date=due_date
            )
            self.db_session.add(task)
            self.db_session.flush() 
            
            notif_controller = NotificationController(self.db_session)

            if assigned_user_ids:
                for user_id in assigned_user_ids:
                    assignment = TaskAssignment(
                        task_id=task.id,
                        user_id=user_id
                    )
                    self.db_session.add(assignment)
                    notif=NotificationCreate(
                        user_id=user_id,
                        message=f"You have been assigned to task '{name}'",)
                    notif_controller.create_notification(notif )
            self.db_session.commit()
            self.db_session.refresh(task)
            return task
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by ID.

        Args:
            task_id (int): Task ID.

        Returns:
            Optional[Task]: Task object if found, otherwise None.
        """
        return self.db_session.query(Task).filter(Task.id == task_id).first()
    
    def get_task_with_details(self, task_id: int) -> Optional[TaskDetailResponse]:
        """
        Retrieve a task with all its related details.
        
        Args:
            task_id (int): Task ID
            
        Returns:
            Optional[TaskDetailResponse]: Detailed task response if found
        """
        # Get the basic task
        task = self.db_session.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            return None
            
        # Get assigned users with details
        assigned_users = self.db_session.query(User).join(
            TaskAssignment, TaskAssignment.user_id == User.id
        ).filter(
            TaskAssignment.task_id == task_id
        ).all()
        
        # Get comments with user info
        comments = self.db_session.query(Comment).filter(
            Comment.task_id == task_id
        ).all()
        
        # Get file attachments
        attachments = self.db_session.query(FileAttachment).filter(
            FileAttachment.task_id == task_id
        ).all()
        
        # Get project info
        project = self.db_session.query(Project).filter(
            Project.id == task.project_id
        ).first()
        
        # Create response DTO
        task_base = TaskDetailResponse.from_orm(task)
        
        # Add relationships
        task_base.assigned_users_details = assigned_users
        task_base.comments = comments
        task_base.attachments = attachments
        task_base.project = project
        
        # Set the assigned user IDs
        task_base.assigned_users = [user.id for user in assigned_users]
        
        return task_base
    
    def get_task_assignments(self, task_id: int) -> List[int]:
        """
        Get list of user IDs assigned to a task.

        Args:
            task_id (int): Task ID

        Returns:
            List[int]: List of assigned user IDs
        """
        assignments = self.db_session.query(TaskAssignment.user_id).filter(
            TaskAssignment.task_id == task_id
        ).all() 
        
        return [assignment[0] for assignment in assignments]
    
    def get_tasks_by_project(self, project_id: int) -> List[Task]:
        """
        Get all tasks for a specific project.

        Args:
            project_id (int): Project ID

        Returns:
            List[Task]: List of tasks in the project
        """
        return self.db_session.query(Task).filter(Task.project_id == project_id).all()
    
    def get_tasks_by_user(self, user_id: int) -> List[Task]:
        """
        Get all tasks assigned to a specific user.

        Args:
            user_id (int): User ID

        Returns:
            List[Task]: List of tasks assigned to the user
        """
        tasks = self.db_session.query(Task).join(
            TaskAssignment, TaskAssignment.task_id == Task.id
        ).filter(
            TaskAssignment.user_id == user_id
        ).all()
        return tasks
    
    def get_tasks_paginated(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[List[str]] = None,
        priority: Optional[List[str]] = None,
        due_date_from: Optional[date] = None,
        due_date_to: Optional[date] = None,
        assigned_to_user_id: Optional[int] = None,
        project_id: Optional[int] = None,
        search_term: Optional[str] = None
    ) -> Tuple[List[TaskResponse], int]:
        """
        Get paginated list of tasks with optional filtering, including assigned user IDs.
        """

        query = self.db_session.query(Task)

        if status:
            query = query.filter(Task.status.in_(status))

        if priority:
            query = query.filter(Task.priority.in_(priority))

        if due_date_from:
            query = query.filter(Task.due_date >= due_date_from)

        if due_date_to:
            query = query.filter(Task.due_date <= due_date_to)

        if project_id:
            query = query.filter(Task.project_id == project_id)

        if assigned_to_user_id:
            query = query.join(TaskAssignment).filter(TaskAssignment.user_id == assigned_to_user_id)

        if search_term:
            search_pattern = f"%{search_term}%"
            query = query.filter(or_(
                Task.name.ilike(search_pattern),
                Task.description.ilike(search_pattern)
            ))

        total = query.count()

        offset = (page - 1) * page_size

        # Eagerly load assignments to reduce number of queries
        tasks = query.order_by(Task.updated_at.desc()).offset(offset).limit(page_size).all()

        task_responses = []
        for task in tasks:
            assigned_user_ids = self.get_task_assignments(task.id)
            task_responses.append(TaskResponse(
                id=task.id,
                name=task.name,
                description=task.description,
                priority=task.priority,
                status=task.status,
                due_date=task.due_date,
                created_at=str(task.created_at),
                updated_at=str(task.updated_at),
                assigned_users=assigned_user_ids,
                project_id=task.project_id
            ))

        return task_responses, total

    def update_task(self, 
                   task_id: int, 
                   update_data: Dict[str, Any],
                   assigned_user_ids: Optional[List[int]] = None) -> Optional[Task]:
        """
        Update a task and its assignments.

        Args:
            task_id (int): Task ID to update
            update_data (Dict[str, Any]): Task fields to update
            assigned_user_ids (Optional[List[int]]): List of user IDs to assign

        Returns:
            Optional[Task]: Updated task object if found, otherwise None
        """
        try:
            task = self.get_task_by_id(task_id)
            if not task:
                return None
            
            # Update task fields
            for key, value in update_data.items():
                if hasattr(task, key) and value is not None:
                    setattr(task, key, value)
                    
            # Update task assignments (nese jon)
            if assigned_user_ids is not None:
                # Remove existing assignments
                self.db_session.query(TaskAssignment).filter(
                    TaskAssignment.task_id == task_id
                ).delete()
                notif_controller = NotificationController(self.db_session)
                # Create new assignments
                for user_id in assigned_user_ids:
                    assignment = TaskAssignment(
                        task_id=task_id,
                        user_id=user_id
                    )
                    self.db_session.add(assignment)
                    notif=NotificationCreate(
                        user_id=user_id,
                        message=f"Theres an update on task: '{task.name}'",)
                    notif_controller.create_notification(notif )
            
            self.db_session.commit()
            self.db_session.refresh(task)
            return task
        except Exception as e:
            self.db_session.rollback()
            raise e

    def delete_task(self, task_id: int) -> Optional[Task]:
        """
        Delete a task and its assignments by ID.

        Args:
            task_id (int): ID of the task to delete

        Returns:
            Optional[Task]: Deleted task object if found, otherwise None
        """
        try:
            task = self.get_task_by_id(task_id)
            if task:
                # Delete all task assignments first (shkaku i foreign keys)
                self.db_session.query(TaskAssignment).filter(
                    TaskAssignment.task_id == task_id
                ).delete()
                
               
                self.db_session.delete(task)
                self.db_session.commit()
                return task
            return None
        except Exception as e:
            self.db_session.rollback()
            raise e
    
    def get_task_statistics(self) -> TaskStatistics:
        """
        Get statistics about tasks in the system.
        
        Returns:
            TaskStatistics: Statistics about tasks
        """
        # Total tasks
        total_tasks = self.db_session.query(func.count(Task.id)).scalar()
        
        # Completed tasks
        completed_tasks = self.db_session.query(func.count(Task.id)).filter(
            Task.status == StatusEnum.DONE.value
        ).scalar()
        
        # Overdue tasks
        today = date.today()
        overdue_tasks = self.db_session.query(func.count(Task.id)).filter(
            Task.due_date < today,
            Task.status != StatusEnum.DONE.value
        ).scalar()
        
        # Tasks by status
        status_counts = {}
        for status in StatusEnum:
            count = self.db_session.query(func.count(Task.id)).filter(
                Task.status == status.value
            ).scalar()
            status_counts[status.value] = count
        
        # Tasks by priority
        priority_counts = {
            "Low": self.db_session.query(func.count(Task.id)).filter(Task.priority == "Low").scalar(),
            "Medium": self.db_session.query(func.count(Task.id)).filter(Task.priority == "Medium").scalar(),
            "High": self.db_session.query(func.count(Task.id)).filter(Task.priority == "High").scalar()
        }
        
        return TaskStatistics(
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            overdue_tasks=overdue_tasks,
            tasks_by_status=status_counts,
            tasks_by_priority=priority_counts
        )