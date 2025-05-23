from typing import List, Callable
from fastapi import HTTPException, Depends, Request, status
from sqlalchemy.orm import Session
from sqlalchemy import select, exists, and_, or_
from app.auth import auth_service
from app.models.user_role import UserRole
from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.models.task import Task
from app.models.task_assignment import TaskAssignment
from app.models.project import Project

class PermissionChecker:
    """
    Handles authorization logic for checking user permissions.
    """
    
    @staticmethod
    async def check_permission(permission_name: str, db: Session, user_id: int) -> bool:
        """
        Check if a user has a specific permission.
        
        Args:
            permission_name (str): The name of the permission to check
            db (Session): Database session
            user_id (int): User ID to check permissions for
            
        Returns:
            bool: True if the user has the permission, False otherwise
        """
        # Using SQLAlchemy ORM to check if user has the permission through their roles
        stmt = select(exists().where(
            and_(
                UserRole.user_id == user_id,
                UserRole.role_id == RolePermission.role_id,
                RolePermission.permission_id == Permission.id,
                Permission.name == permission_name
            )
        ))
        
        has_permission = db.scalar(stmt)
        return has_permission
    
    @classmethod
    def require_permission(cls, permission_name: str):
        """
        Dependency that checks if a user has the required permission.
        
        Args:
            permission_name (str): The permission required to access the endpoint
            
        Returns:
            Callable: A dependency function that checks the permission
        """
        async def permission_dependency(
            request: Request,
            user_data: dict = Depends(auth_service.verify_user)
        ) -> dict:
            user_id = user_data.get("user_id")
            db = request.state.db
            
            has_permission = await cls.check_permission(permission_name, db, user_id)
            
            if not has_permission:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied: {permission_name} required"
                )
            
            return user_data
        
        return permission_dependency
    
    @classmethod
    def require_permissions(cls, permission_names: List[str], require_all: bool = True):
        """
        Dependency that checks if a user has multiple required permissions.
        
        Args:
            permission_names (List[str]): The permissions required to access the endpoint
            require_all (bool): If True, the user must have all permissions; if False, any one is sufficient
            
        Returns:
            Callable: A dependency function that checks the permissions
        """
        async def permissions_dependency(
            request: Request,
            user_data: dict = Depends(auth_service.verify_user)
        ) -> dict:
            user_id = user_data.get("user_id")
            db = request.state.db
            
            permissions_satisfied = []
            
            for permission_name in permission_names:
                has_permission = await cls.check_permission(permission_name, db, user_id)
                permissions_satisfied.append(has_permission)
            
            if require_all and not all(permissions_satisfied):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied: All of {', '.join(permission_names)} required"
                )
                
            if not require_all and not any(permissions_satisfied):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied: At least one of {', '.join(permission_names)} required"
                )
            
            return user_data
        
        return permissions_dependency
    
    @classmethod
    def check_resource_ownership(cls, resource_type: str, resource_id_param: str = None):
        """
        Dependency that checks if a user owns or can access a specific resource.
        
        Args:
            resource_type (str): The type of resource (e.g., 'task', 'project')
            resource_id_param (str): The name of the path parameter for the resource ID
            
        Returns:
            Callable: A dependency function that checks resource ownership
        """
        async def ownership_dependency(
            request: Request,
            user_data: dict = Depends(auth_service.verify_user)
        ) -> dict:
            user_id = user_data.get("user_id")
            db = request.state.db
            
            # Get resource ID from path parameters
            if resource_id_param:
                resource_id = request.path_params.get(resource_id_param)
                if not resource_id:
                    return user_data  # If no resource ID, just return the user data
                
                # Check ownership based on resource type
                if resource_type == "task":
                    # Check if user is assigned to the task or has admin/manager role
                    admin_manager_stmt = select(exists().where(
                        and_(
                            UserRole.user_id == user_id,
                            UserRole.role_id == Role.id,
                            Role.name.in_(['Admin', 'Manager'])
                        )
                    ))
                    
                    task_access_stmt = select(exists().where(
                        and_(
                            Task.id == resource_id,
                            or_(
                                and_(
                                    TaskAssignment.task_id == Task.id,
                                    TaskAssignment.user_id == user_id
                                ),
                                admin_manager_stmt.scalar_subquery()
                            )
                        )
                    ))
                    
                    has_access = db.scalar(task_access_stmt)
                    
                elif resource_type == "project":
                    # Check if user has admin/manager role for project access
                    project_access_stmt = select(exists().where(
                        and_(
                            Project.id == resource_id,
                            select(exists().where(
                                and_(
                                    UserRole.user_id == user_id,
                                    UserRole.role_id == Role.id,
                                    Role.name.in_(['Admin', 'Manager'])
                                )
                            )).scalar_subquery()
                        )
                    ))
                    
                    has_access = db.scalar(project_access_stmt)
                    
                elif resource_type == "user":
                    # Special case for user resources - users can access their own profile
                    has_access = int(resource_id) == user_id or await cls.check_permission("read_any_user", db, user_id)
                    
                else:
                    # Default to admin check for unknown resource types
                    admin_check_stmt = select(exists().where(
                        and_(
                            UserRole.user_id == user_id,
                            UserRole.role_id == Role.id,
                            Role.name == 'Admin'
                        )
                    ))
                    
                    has_access = db.scalar(admin_check_stmt)
                
                if not has_access:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Access denied: You don't have permission to access this {resource_type}"
                    )
            
            return user_data
        
        return ownership_dependency