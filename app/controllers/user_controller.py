from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.repositories import UserRepository
from app.utils import get_db, get_global_db
from app.models.dtos import UserCreate, UserUpdate, UserResponse, TenantUserCreate
from typing import List, Optional
from app.repositories.tenant_user_repository import TenantUserRepository
from app.models.dtos.role_dtos import RoleResponse
from fastapi import BackgroundTasks
from app.utils.email_utils import send_account_creation_email


class UserController:
    """Controller class for handling user operations."""

    def __init__(self, db_session: Session = Depends(get_db)):
        """Initialize the UserController."""
        self.repository = UserRepository(db_session)



    def create_user(self, user_create: UserCreate, current_user: dict, default_role_id: Optional[int] = None) -> UserResponse:
        """Create a new user, assign default roles, and send a welcome email."""
        user = self.repository.create_user(
            email=user_create.email,
            password=user_create.password,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            department_id=user_create.department_id,
            team_id=user_create.team_id
        )

        # Assign default role
        if default_role_id:
            self.repository.assign_role_to_user(user.id, default_role_id)
        else:
            employee_role = self.repository.get_role_by_name("Employee")
            if employee_role:
                self.repository.assign_role_to_user(user.id, employee_role.id)
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Default 'Employee' role not found. Unable to assign default role."
                )

        # Global DB for tenant linkage
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

        # Send welcome email asynchronously without blocking
        send_account_creation_email(
        to_email=user_create.email,
        first_name=user_create.first_name,
        password=user_create.password
        )


        # Attach role_id to the response
        roles = self.repository.get_user_roles(user.id)
        role_id = roles[0].id if roles else None

        response = UserResponse.from_orm(user)
        response.role_id = role_id
        return response

    def get_user(self, user_id: int) -> UserResponse:
        """Get a user by ID."""
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        roles = self.repository.get_user_roles(user.id)
        role_id = roles[0].id if roles else None

        response = UserResponse.from_orm(user)
        response.role_id = role_id
        return response

    def update_user(self, user_id: int, user_update: UserUpdate) -> UserResponse:
        """Update a user's information."""
        user = self.repository.update_user(
            user_id,
            first_name=user_update.first_name,
            last_name=user_update.last_name,
            department_id=user_update.department_id,
            team_id=user_update.team_id
        )
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        roles = self.repository.get_user_roles(user.id)
        role_id = roles[0].id if roles else None

        response = UserResponse.from_orm(user)
        response.role_id = role_id
        return response

    def delete_user(self, user_id: int) -> dict:
        """Delete a user."""
        user = self.repository.delete_user(user_id)
        if user:
            return {"message": "User deleted successfully"}
        raise HTTPException(status_code=404, detail="User not found")

    def assign_role_to_user(self, user_id: int, role_id: int) -> dict:
        """Assign a role to a user."""
        success = self.repository.assign_role_to_user(user_id, role_id)
        if success:
            return {"message": "Role assigned successfully"}
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to assign role to user")

    def remove_role_from_user(self, user_id: int, role_id: int) -> dict:
        """Remove a role from a user."""
        success = self.repository.remove_role_from_user(user_id, role_id)
        if success:
            return {"message": "Role removed successfully"}
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to remove role from user")

    def get_user_roles(self, user_id: int) -> List[RoleResponse]:
        """Get all roles assigned to a user."""
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        roles = self.repository.get_user_roles(user_id)
        return [RoleResponse.from_orm(role) for role in roles]

    def get_user_by_email(self, email: str) -> UserResponse:
        """Get a user by email."""
        user = self.repository.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        roles = self.repository.get_user_roles(user.id)
        role_id = roles[0].id if roles else None

        response = UserResponse.from_orm(user)
        response.role_id = role_id
        return response

    def get_all_users(self) -> List[UserResponse]:
        """Retrieve all users in the system."""
        users = self.repository.get_all_users()
        responses = []

        for user in users:
            roles = self.repository.get_user_roles(user.id)
            role_id = roles[0].id if roles else None

            response = UserResponse.from_orm(user)
            response.role_id = role_id
            responses.append(response)

        return responses
