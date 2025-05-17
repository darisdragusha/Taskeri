from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.user import User
from app.models.tenant.roles.role import Role
from app.models.user_role import UserRole
from app.utils import hash_password
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
import logging

# Configure logging
logger = logging.getLogger(__name__)

class UserRepository:
    """Repository class for handling user-related database operations."""

    def __init__(self, db_session: Session):
        """
        Initialize the UserRepository.

        Args:
            db_session (Session): SQLAlchemy database session.
        """
        self.db_session = db_session

    def create_user(self, email: str, password: str, first_name: str, last_name: str, department_id: Optional[int], team_id: Optional[int]) -> User:
        """
        Create a new user.

        Args:
            email (str): User's email.
            password (str): User's password (plaintext).
            first_name (str): User's first name.
            last_name (str): User's last name.
            department_id (Optional[int]): Associated department ID.
            team_id (Optional[int]): Associated team ID.

        Returns:
            User: The newly created user object.
        """
        hashed_password = hash_password(password)
        user = User(
            email=email,
            password_hash=hashed_password,
            first_name=first_name,
            last_name=last_name,
            department_id=department_id,
            team_id=team_id
        )
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by ID.

        Args:
            user_id (int): User ID.

        Returns:
            Optional[User]: User object if found, otherwise None.
        """
        return self.db_session.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by email.

        Args:
            email (str): User email.

        Returns:
            Optional[User]: User object if found, otherwise None.
        """
        return self.db_session.query(User).filter(User.email == email).first()

    def update_user(self, user_id: int, first_name: Optional[str] = None, last_name: Optional[str] = None, department_id: Optional[int] = None, team_id: Optional[int] = None) -> Optional[User]:
        """
        Update an existing user's details.

        Args:
            user_id (int): ID of the user to update.
            first_name (Optional[str]): New first name.
            last_name (Optional[str]): New last name.
            department_id (Optional[int]): New department ID.
            team_id (Optional[int]): New team ID.

        Returns:
            Optional[User]: Updated user object if found, otherwise None.
        """
        user = self.get_user_by_id(user_id)
        if user:
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if department_id:
                user.department_id = department_id
            if team_id:
                user.team_id = team_id
            self.db_session.commit()
            self.db_session.refresh(user)
            return user
        return None

    def delete_user(self, user_id: int) -> Optional[User]:
        """
        Delete a user by ID.

        Args:
            user_id (int): ID of the user to delete.

        Returns:
            Optional[User]: Deleted user object if found, otherwise None.
        """
        user = self.get_user_by_id(user_id)
        if user:
            self.db_session.delete(user)
            self.db_session.commit()
            return user
        return None
        
    def get_role_by_name(self, role_name: str) -> Optional[Role]:
        """
        Get a role by its name.
        
        Args:
            role_name (str): Name of the role.
            
        Returns:
            Optional[Role]: Role object if found, otherwise None.
        """
        return self.db_session.query(Role).filter(Role.name == role_name).first()
        
    def get_user_roles(self, user_id: int) -> List[Role]:
        """
        Get all roles assigned to a user.
        
        Args:
            user_id (int): User ID.
            
        Returns:
            List[Role]: List of roles assigned to the user.
        """
        roles = self.db_session.query(Role).join(
            UserRole, UserRole.role_id == Role.id
        ).filter(
            UserRole.user_id == user_id
        ).all()
        
        return roles
        
    def assign_role_to_user(self, user_id: int, role_id: int) -> bool:
        """
        Assign a role to a user.
        
        Args:
            user_id (int): User ID.
            role_id (int): Role ID.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Check if user and role exist
            user = self.get_user_by_id(user_id)
            role = self.db_session.query(Role).filter(Role.id == role_id).first()
            
            if not user or not role:
                return False
                
            # Check if the user already has this role
            existing = self.db_session.query(UserRole).filter(
                UserRole.user_id == user_id,
                UserRole.role_id == role_id
            ).first()
            
            if existing:
                return True  # Role already assigned
                
            # Create the new role assignment
            user_role = UserRole(
                user_id=user_id,
                role_id=role_id
            )
            
            self.db_session.add(user_role)
            self.db_session.commit()
            return True
            
        except SQLAlchemyError as e:
            logger.error(f"Error assigning role to user {user_id}: {e}")
            self.db_session.rollback()
            return False
            
    def remove_role_from_user(self, user_id: int, role_id: int) -> bool:
        """
        Remove a role from a user.
        
        Args:
            user_id (int): User ID.
            role_id (int): Role ID.
            
        Returns:
            bool: True if successful, False otherwise.
        """
        try:
            # Find the role assignment
            role_assignment = self.db_session.query(UserRole).filter(
                UserRole.user_id == user_id,
                UserRole.role_id == role_id
            ).first()
            
            if not role_assignment:
                return False  # Role not assigned to user
                
            # Remove the role assignment
            self.db_session.delete(role_assignment)
            self.db_session.commit()
            return True
            
        except SQLAlchemyError:
            self.db_session.rollback()
            return False
