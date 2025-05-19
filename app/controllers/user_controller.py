from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.repositories import UserRepository
from app.utils import get_db, get_global_db
from app.models.dtos import UserCreate, UserUpdate, UserResponse, TenantUserCreate
from typing import List, Optional, Dict
from app.repositories.tenant_user_repository import TenantUserRepository
from app.auth import auth_service

class UserController:
    """Controller class for handling user operations."""

    def __init__(self, db_session: Session = Depends(get_db)):
        """
        Initialize the UserController.

        Args:
            db_session (Session): SQLAlchemy database session.
        """
        self.repository = UserRepository(db_session)

    def create_user(self, user_create: UserCreate, current_user: dict, default_role_id: Optional[int] = None) -> UserResponse:
        """
        Create a new user and assign them default roles.

        Args:
            user_create (UserCreate): Data for the new user.
            default_role_id (Optional[int]): ID of the default role to assign to the user.
                                            If None, will use Employee role by default.

        Returns:
            UserResponse: Created user response.
        """
        # Create the user first
        user = self.repository.create_user(
            email=user_create.email,
            password=user_create.password,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            department_id=user_create.department_id,
            team_id=user_create.team_id
        )
        
        # Assign default role if specified, otherwise find the "Employee" role
        if default_role_id:
            self.repository.assign_role_to_user(user.id, default_role_id)
        else:
            # Try to find Employee role by name and assign it
            employee_role = self.repository.get_role_by_name("Employee")
            if employee_role:
                self.repository.assign_role_to_user(user.id, employee_role.id)
            else:
                # Log a warning or raise an exception if the Employee role is not found
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Default 'Employee' role not found. Unable to assign default role."
                )
        
        schema_name = current_user["tenant_name"]

        with get_global_db() as global_db:
            tenant_user_repo = TenantUserRepository(global_db)
            tenant_user_repo.create(
                user_data=TenantUserCreate(
                    email=user_create.email,
                    first_name=user_create.first_name,
                    last_name=user_create.last_name,
                    password=user_create.password,
                    tenant_schema=schema_name
                )
            )

        return UserResponse.from_orm(user)

    def get_user(self, user_id: int) -> UserResponse:
        """
        Get a user by ID.

        Args:
            user_id (int): User ID.

        Returns:
            UserResponse: Retrieved user response.
        """
        user = self.repository.get_user_by_id(user_id)
        if user:
            return UserResponse.from_orm(user)
        raise HTTPException(status_code=404, detail="User not found")

    def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        """
        Update a user's information.

        Args:
            user_id (int): User ID.
            user_update (UserUpdate): Updated user data.

        Returns:
            UserResponse: Updated user response.
        """
        user = self.repository.update_user(
            user_id,
            first_name=user_update.first_name,
            last_name=user_update.last_name,
            department_id=user_update.department_id,
            team_id=user_update.team_id
        )
        if user:
            return UserResponse.from_orm(user)
        raise HTTPException(status_code=404, detail="User not found")

    def delete_user(self, user_id: int) -> dict:
        """
        Delete a user.

        Args:
            user_id (int): User ID.

        Returns:
            dict: Success message.
        """
        user = self.repository.delete_user(user_id)
        if user:
            return {"message": "User deleted successfully"}
        raise HTTPException(status_code=404, detail="User not found")
        
    def assign_role_to_user(self, user_id: int, role_id: int) -> dict:
        """
        Assign a role to a user.
        
        Args:
            user_id (int): User ID.
            role_id (int): Role ID.
            
        Returns:
            dict: Success message.
        """
        success = self.repository.assign_role_to_user(user_id, role_id)
        if success:
            return {"message": "Role assigned successfully"}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Failed to assign role to user"
        )
        
    def remove_role_from_user(self, user_id: int, role_id: int) -> dict:
        """
        Remove a role from a user.
        
        Args:
            user_id (int): User ID.
            role_id (int): Role ID.
            
        Returns:
            dict: Success message.
        """
        success = self.repository.remove_role_from_user(user_id, role_id)
        if success:
            return {"message": "Role removed successfully"}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Failed to remove role from user"
        )
        
    def get_user_roles(self, user_id: int) -> List[Dict[str, str]]:
        """
        Get all roles assigned to a user.
        
        Args:
            user_id (int): User ID.
            
        Returns:
            List[Dict[str, str]]: List of roles with their details.
        """
        # Check if user exists
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Get user roles
        roles = self.repository.get_user_roles(user_id)
        return [{"id": role.id, "name": role.name} for role in roles]
    
    def get_user_by_email(self, email: str) -> UserResponse:
        """
        Get a user by email.

        Args:
            email (str): User email.

        Returns:
            UserResponse: Retrieved user response.
        """
        user = self.repository.get_user_by_email(email)
        if user:
            return UserResponse.from_orm(user)
        raise HTTPException(status_code=404, detail="User not found")
