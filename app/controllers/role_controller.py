from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from repositories.role_repository import RoleRepository
from utils.db_utils import get_db
from models.dtos.role_dtos import RoleCreate, RoleUpdate, RoleResponse

class RoleController:
    """Controller class for handling role operations."""

    def __init__(self, db_session: Session = Depends(get_db)):
        """
        Initialize the RoleController.

        Args:
            db_session (Session): SQLAlchemy database session.
        """
        self.repository = RoleRepository(db_session)

    def create_role(self, role_create: RoleCreate) -> RoleResponse:
        """
        Create a new role.

        Args:
            role_create (RoleCreate): Data for the new role.

        Returns:
            RoleResponse: Created role response.
        """
        role = self.repository.create_role(name=role_create.name)
        return RoleResponse.from_orm(role)

    def get_role(self, role_id: int) -> RoleResponse:
        """
        Get a role by ID.

        Args:
            role_id (int): Role ID.

        Returns:
            RoleResponse: Retrieved role response.
        """
        role = self.repository.get_role_by_id(role_id)
        if role:
            return RoleResponse.from_orm(role)
        raise HTTPException(status_code=404, detail="Role not found")

    def update_role(self, role_id: int, role_update: RoleUpdate) -> RoleResponse:
        """
        Update a role's information.

        Args:
            role_id (int): Role ID.
            role_update (RoleUpdate): Updated role data.

        Returns:
            RoleResponse: Updated role response.
        """
        role = self.repository.update_role(role_id, name=role_update.name)
        if role:
            return RoleResponse.from_orm(role)
        raise HTTPException(status_code=404, detail="Role not found")

    def delete_role(self, role_id: int) -> dict:
        """
        Delete a role.

        Args:
            role_id (int): Role ID.

        Returns:
            dict: Success message.
        """
        role = self.repository.delete_role(role_id)
        if role:
            return {"message": "Role deleted successfully"}
        raise HTTPException(status_code=404, detail="Role not found")
