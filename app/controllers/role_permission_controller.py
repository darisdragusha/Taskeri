from sqlalchemy.orm import Session
from repositories.role_permission_repository import RolePermissionRepository
from models.dtos.role_permission_dto import RolePermissionCreate
from models.role_permission import RolePermission
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
