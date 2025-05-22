from sqlalchemy.orm import Session
from app.repositories.role_permission_repository import RolePermissionRepository
from app.models.dtos.role_permission_dto import RolePermissionCreate
from app.models.role_permission import RolePermission
from app.models.permission import Permission  # if not already imported
from typing import List

class RolePermissionController:
    """
    Controller for managing role-permission assignments.
    """

    def __init__(self, db: Session):
        """
        Initialize the controller with a database session.
        """
        self.repo = RolePermissionRepository(db)

    def create_mapping(self, data: RolePermissionCreate) -> RolePermission:
        """
        Assign a permission to a role.

        :param data: DTO with role_id and permission_id
        :return: Created RolePermission object
        """
        return self.repo.create(data)

    def get_all_mappings(self) -> List[RolePermission]:
        """
        Retrieve all role-permission mappings.

        :return: List of RolePermission objects
        """
        return self.repo.get_all()

    def delete_mapping(self, role_id: int, permission_id: int) -> bool:
        """
        Delete a specific role-permission mapping.

        :param role_id: ID of the role
        :param permission_id: ID of the permission
        :return: True if deleted, False otherwise
        """
        return self.repo.delete(role_id, permission_id)
    

    def get_permissions_by_role_id(self, role_id: int) -> List[Permission]:
        """
        Get list of Permission entities assigned to the role.

        :param role_id: ID of the role
        :return: List of Permission objects
        """
        return self.repo.get_permissions_by_role_id(role_id)
