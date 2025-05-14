from models.dtos import TenantUserCreate, TenantUserOut
from repositories import TenantUserRepository
from repositories.user_repository import UserRepository
from repositories.permission_repository import PermissionRepository
from repositories.role_repository import RoleRepository
from utils.db_utils import get_tenant_scoped_session
from repositories.role_permission_repository import RolePermissionRepository
from models.dtos.role_permission_dto import RolePermissionCreate
from services.tenant_provisioning import create_new_tenant
from sqlalchemy.orm import Session
from fastapi import HTTPException


class TenantUserController:
    def __init__(self, db: Session):
        self.repo = TenantUserRepository(db)

    def register_tenant_user(self, user_data: TenantUserCreate) -> TenantUserOut:
        if self.repo.get_by_email(user_data.email):
            raise HTTPException(status_code=400, detail="Email already exists.")

        create_new_tenant(self.repo.db, user_data.tenant_schema)
        user = self.repo.create(user_data)

        tenant_db = get_tenant_scoped_session("tenant_"+user_data.tenant_schema)

        PERMISSIONS = [
            "read_company", "create_company", "update_company", "delete_company",
            "read_role", "create_role", "update_role", "delete_role",
            "read_any_user", "create_user", "read_user", "update_user", "delete_user",
            "manage_user_roles",
            "read_task", "create_task", "update_task", "delete_own_task", "delete_any_task",
            "read_any_task", "read_any_user_task", "view_statistics",
            "read_permission", "create_permission", "update_permission", "delete_permission",
            "create_comment", "read_comment", "update_comment", "delete_comment"
        ]

        permission_repo = PermissionRepository(tenant_db)
        permission_repo.create_permissions_bulk(PERMISSIONS)

        ROLES = [
            "Admin", "Manager", "Employee"
        ]
        role_repo = RoleRepository(tenant_db)
        role_repo.create_roles_bulk(ROLES)

        all_roles = role_repo.list_roles()
        all_permissions = permission_repo.list_permissions()

        role_id_map = {role.name.lower(): role.id for role in all_roles}
        perm_name_map = {perm.name: perm.id for perm in all_permissions}

        role_permission_data = []

        for perm_name, perm_id in perm_name_map.items():
            # Admin gets all
            role_permission_data.append(RolePermissionCreate(role_id=role_id_map["admin"], permission_id=perm_id))

            if any(kw in perm_name for kw in ["read_", "view_", "manage_"]):
                role_permission_data.append(RolePermissionCreate(role_id=role_id_map["manager"], permission_id=perm_id))

            if perm_name in [
                "read_task", "create_task", "update_task", "delete_own_task",
                "read_comment", "create_comment", "update_comment"
            ]:
                role_permission_data.append(RolePermissionCreate(role_id=role_id_map["employee"], permission_id=perm_id))

        role_perm_repo = RolePermissionRepository(tenant_db)
        role_perm_repo.create_bulk(role_permission_data)

        tenant_repo = UserRepository(tenant_db)
        tenant_repo.create_user(
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            password=user_data.password,  
            department_id=None,
            team_id=None
        )
        
        user_id = tenant_repo.get_user_by_email(user_data.email)
        role_id = role_repo.get_role_by_name("Admin")

        tenant_repo.assign_role_to_user(user_id.id, role_id.id)
        return TenantUserOut.model_validate(user)
