from sqlalchemy.orm import Session
from typing import Optional, List
from models.tenant.roles.permission import Permission

class PermissionRepository:
    """Repository class for handling permission-related database operations."""

    def __init__(self, db_session: Session):
        """
        Initialize the PermissionRepository.

        Args:
            db_session (Session): SQLAlchemy database session.
        """
        self.db_session = db_session

    def create_permission(self, name: str) -> Permission:
        """
        Create a new permission.

        Args:
            name (str): Name of the permission.

        Returns:
            Permission: The newly created permission object.
        """
        permission = Permission(name=name)
        self.db_session.add(permission)
        self.db_session.commit()
        self.db_session.refresh(permission)
        return permission
    
    def create_permissions_bulk(self, names: List[str]) -> List[Permission]:
        """
        Create multiple permissions in bulk.

        Args:
            names (List[str]): List of permission names.

        Returns:
            List[Permission]: List of created Permission objects.
        """
        permissions = [Permission(name=name) for name in names]
        self.db_session.bulk_save_objects(permissions)
        self.db_session.commit()

        # Optional: re-query to get full objects with IDs
        return self.db_session.query(Permission).filter(Permission.name.in_(names)).all()


    def get_permission_by_id(self, permission_id: int) -> Optional[Permission]:
        """
        Retrieve a permission by ID.

        Args:
            permission_id (int): Permission ID.

        Returns:
            Optional[Permission]: Permission object if found, otherwise None.
        """
        return self.db_session.query(Permission).filter(Permission.id == permission_id).first()

    def get_permission_by_name(self, name: str) -> Optional[Permission]:
        """
        Retrieve a permission by name.

        Args:
            name (str): Name of the permission.

        Returns:
            Optional[Permission]: Permission object if found, otherwise None.
        """
        return self.db_session.query(Permission).filter(Permission.name == name).first()

    def list_permissions(self) -> List[Permission]:
        """
        List all permissions.

        Returns:
            List[Permission]: All permission objects.
        """
        return self.db_session.query(Permission).all()

    def update_permission(self, permission_id: int, name: str) -> Optional[Permission]:
        """
        Update an existing permission's name.

        Args:
            permission_id (int): ID of the permission to update.
            name (str): New permission name.

        Returns:
            Optional[Permission]: Updated permission object if found, otherwise None.
        """
        permission = self.get_permission_by_id(permission_id)
        if permission:
            permission.name = name
            self.db_session.commit()
            self.db_session.refresh(permission)
            return permission
        return None

    def delete_permission(self, permission_id: int) -> Optional[Permission]:
        """
        Delete a permission by ID.

        Args:
            permission_id (int): ID of the permission to delete.

        Returns:
            Optional[Permission]: Deleted permission object if found, otherwise None.
        """
        permission = self.get_permission_by_id(permission_id)
        if permission:
            self.db_session.delete(permission)
            self.db_session.commit()
            return permission
        return None
