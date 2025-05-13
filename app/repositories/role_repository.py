from sqlalchemy.orm import Session
from typing import Optional, List
from models.tenant.roles.role import Role  # Adjust path if needed

class RoleRepository:
    """Repository class for handling role-related database operations."""

    def __init__(self, db_session: Session):
        """
        Initialize the RoleRepository.

        Args:
            db_session (Session): SQLAlchemy database session.
        """
        self.db_session = db_session

    def create_role(self, name: str) -> Role:
        """
        Create a new role.

        Args:
            name (str): Name of the role.

        Returns:
            Role: The newly created role object.
        """
        role = Role(name=name)
        self.db_session.add(role)
        self.db_session.commit()
        self.db_session.refresh(role)
        return role
    
    def create_roles_bulk(self, names: List[str]) -> List[Role]:
        """
        Create multiple roles in bulk.

        Args:
            names (List[str]): List of role names.

        Returns:
            List[Role]: List of created roles objects.
        """
        roles = [Role(name=name) for name in names]
        self.db_session.bulk_save_objects(roles)
        self.db_session.commit()

        # Optional: re-query to get full objects with IDs
        return self.db_session.query(Role).filter(Role.name.in_(names)).all()
    
    def get_role_by_id(self, role_id: int) -> Optional[Role]:
        """
        Retrieve a role by ID.

        Args:
            role_id (int): Role ID.

        Returns:
            Optional[Role]: Role object if found, otherwise None.
        """
        return self.db_session.query(Role).filter(Role.id == role_id).first()

    def get_role_by_name(self, name: str) -> Optional[Role]:
        """
        Retrieve a role by name.

        Args:
            name (str): Name of the role.

        Returns:
            Optional[Role]: Role object if found, otherwise None.
        """
        return self.db_session.query(Role).filter(Role.name == name).first()

    def list_roles(self) -> List[Role]:
        """
        List all roles.

        Returns:
            List[Role]: All role objects.
        """
        return self.db_session.query(Role).all()

    def update_role(self, role_id: int, name: str) -> Optional[Role]:
        """
        Update an existing role's name.

        Args:
            role_id (int): ID of the role to update.
            name (str): New role name.

        Returns:
            Optional[Role]: Updated role object if found, otherwise None.
        """
        role = self.get_role_by_id(role_id)
        if role:
            role.name = name
            self.db_session.commit()
            self.db_session.refresh(role)
            return role
        return None

    def delete_role(self, role_id: int) -> Optional[Role]:
        """
        Delete a role by ID.

        Args:
            role_id (int): ID of the role to delete.

        Returns:
            Optional[Role]: Deleted role object if found, otherwise None.
        """
        role = self.get_role_by_id(role_id)
        if role:
            self.db_session.delete(role)
            self.db_session.commit()
            return role
        return None