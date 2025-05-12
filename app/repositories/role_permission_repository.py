from sqlalchemy.orm import Session
from models.role_permission import RolePermission
from models.dtos.role_permission_dto import RolePermissionCreate
from typing import List

class RolePermissionRepository:
    """
    Repository for handling role-permission relationship data.
    """

    def __init__(self, db: Session):
        """
        Initialize the repository with the provided database session.
        """
        self.db = db

    def create(self, data: RolePermissionCreate) -> RolePermission:
        """
        Assign a permission to a role.

        :param data: DTO containing role_id and permission_id
        :return: The created RolePermission instance
        """
        role_permission = RolePermission(**data.model_dump())
        self.db.add(role_permission)
        self.db.commit()
        self.db.refresh(role_permission)
        return role_permission

    def get_all(self) -> List[RolePermission]:
        """
        Retrieve all role-permission mappings.

        :return: List of RolePermission objects
        """
        return self.db.query(RolePermission).all()

    def delete(self, role_id: int, permission_id: int) -> bool:
        """
        Remove a permission from a role.

        :param role_id: ID of the role
        :param permission_id: ID of the permission
        :return: True if deleted, False if not found
        """
        mapping = self.db.query(RolePermission).filter_by(
            role_id=role_id, permission_id=permission_id
        ).first()
        if not mapping:
            return False
        self.db.delete(mapping)
        self.db.commit()
        return True