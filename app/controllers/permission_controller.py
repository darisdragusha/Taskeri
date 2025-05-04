from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from repositories.permission_repository import PermissionRepository
from utils.db_utils import get_db
from models.dtos.permission_dtos import PermissionCreate, PermissionUpdate, PermissionResponse

class PermissionController:
    """Controller class for handling permission operations."""

    def __init__(self, db_session: Session = Depends(get_db)):
        """
        Initialize the PermissionController.

        Args:
            db_session (Session): SQLAlchemy database session.
        """
        self.repository = PermissionRepository(db_session)

    def create_permission(self, permission_create: PermissionCreate) -> PermissionResponse:
        """
        Create a new permission.

        Args:
            permission_create (PermissionCreate): Data for the new permission.

        Returns:
            PermissionResponse: Created permission response.
        """
        permission = self.repository.create_permission(name=permission_create.name)
        return PermissionResponse.from_orm(permission)

    def get_permission(self, permission_id: int) -> PermissionResponse:
        """
        Get a permission by ID.

        Args:
            permission_id (int): Permission ID.

        Returns:
            PermissionResponse: Retrieved permission response.
        """
        permission = self.repository.get_permission_by_id(permission_id)
        if permission:
            return PermissionResponse.from_orm(permission)
        raise HTTPException(status_code=404, detail="Permission not found")

    def update_permission(self, permission_id: int, permission_update: PermissionUpdate) -> PermissionResponse:
        """
        Update a permission's information.

        Args:
            permission_id (int): Permission ID.
            permission_update (PermissionUpdate): Updated permission data.

        Returns:
            PermissionResponse: Updated permission response.
        """
        permission = self.repository.update_permission(permission_id, name=permission_update.name)
        if permission:
            return PermissionResponse.from_orm(permission)
        raise HTTPException(status_code=404, detail="Permission not found")

    def delete_permission(self, permission_id: int) -> dict:
        """
        Delete a permission.

        Args:
            permission_id (int): Permission ID.

        Returns:
            dict: Success message.
        """
        permission = self.repository.delete_permission(permission_id)
        if permission:
            return {"message": "Permission deleted successfully"}
        raise HTTPException(status_code=404, detail="Permission not found")
