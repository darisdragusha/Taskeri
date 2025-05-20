from app.models.dtos import TenantUserCreate, TenantUserOut
from app.repositories import TenantUserRepository
from app.repositories.user_repository import UserRepository
from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_repository import RoleRepository
from app.utils.db_utils import get_tenant_session
from app.repositories.role_permission_repository import RolePermissionRepository
from app.models.dtos.role_permission_dto import RolePermissionCreate
from app.services.tenant_provisioning import create_new_tenant
from sqlalchemy.orm import Session
from fastapi import HTTPException

class TenantUserController:
    def __init__(self, db: Session):
        self.repo = TenantUserRepository(db)

    def register_tenant_user(self, user_data: TenantUserCreate) -> TenantUserOut:
        if self.repo.get_by_email(user_data.email):
            raise HTTPException(status_code=400, detail="Email already exists.")

        # Step 1: Create the tenant schema
        create_new_tenant(self.repo.db, user_data.tenant_schema)

        # Step 2: Create the user in the global DB
        user = self.repo.create(user_data)

        # Step 3: Create tenant DB session
        schema_name = "tenant_" + user_data.tenant_schema
        tenant_db = get_tenant_session(schema_name)

        try:
            # Step 4: Create permissions
            PERMISSIONS = [
                "read_company", "create_company", "update_company", "delete_company",
                "read_role", "create_role", "update_role", "delete_role",
                "read_user", "read_any_user", "create_user", "update_user", "update_any_user", "delete_user",
                "manage_user_roles",
                "read_task", "read_any_task", "read_any_user_task", "create_task", "update_task", "update_any_task",
                "delete_own_task", "delete_any_task",
                "view_statistics",
                "read_permission", "create_permission", "update_permission", "delete_permission",
                "create_comment", "read_comment", "update_comment", "delete_comment",
                "check_in", "check_out", "read_own_attendance", "read_any_user_attendance",
                "create_company_settings", "read_company_settings", "update_company_settings", "delete_company_settings",
                "read_department", "create_department", "update_department", "delete_department",
                "read_attachment", "create_attachment", "update_attachment", "delete_attachment",
                "read_invoice", "create_invoice", "update_invoice", "delete_invoice",
                "create_leave_request", "read_leave_request", "update_leave_status",
                "delete_leave_request", "read_any_user_leave_request",
                "read_project", "create_project", "update_project", "update_any_project",
                "delete_project", "delete_any_project",
                "manage_role_permissions",
                "read_team", "create_team", "update_team", "delete_team",
                "create_time_log", "read_time_log", "read_own_time_log", "read_user_time_log",
                "update_time_log", "update_own_time_log", "delete_time_log", "delete_own_time_log",
                "create_user_profile", "read_own_profile", "read_any_profile", "update_own_profile", "update_any_profile",
                "delete_own_profile", "delete_any_profile",
                "assign_user_to_project", "remove_user_from_project", "read_project_users", "read_user_projects"
            ]

            permission_repo = PermissionRepository(tenant_db)
            permission_repo.create_permissions_bulk(PERMISSIONS)

            # Step 5: Create roles
            ROLES = ["Admin", "Manager", "Employee"]
            role_repo = RoleRepository(tenant_db)
            role_repo.create_roles_bulk(ROLES)

            # Step 6: Assign permissions to roles
            all_roles = role_repo.list_roles()
            all_permissions = permission_repo.list_permissions()
            role_id_map = {role.name.lower(): role.id for role in all_roles}
            perm_name_map = {perm.name: perm.id for perm in all_permissions}

            role_permission_data = []

            manager_permissions = [
                "read_company", "read_role", "read_user", "read_any_user", "update_user",
                "read_task", "read_any_task", "read_any_user_task", "create_task", "update_task",
                "update_any_task", "delete_own_task", "read_comment", "create_comment", "update_comment", "delete_comment",
                "read_any_user_attendance", "read_department", "create_department", "update_department", "delete_department",
                "read_attachment", "read_leave_request", "update_leave_status", "read_any_user_leave_request",
                "read_project", "create_project", "update_project", "update_any_project", "delete_project",
                "read_team", "create_team", "update_team", "delete_team", "read_time_log", "read_user_time_log",
                "read_any_profile", "update_any_profile", "assign_user_to_project", "remove_user_from_project",
                "read_project_users", "read_user_projects", "view_statistics"
            ]

            employee_permissions = [
                "read_task", "create_task", "update_task", "delete_own_task",
                "read_comment", "create_comment", "update_comment",
                "check_in", "check_out", "read_own_attendance",
                "create_leave_request", "read_leave_request", "delete_leave_request",
                "create_time_log", "read_own_time_log", "update_own_time_log", "delete_own_time_log",
                "create_user_profile", "read_own_profile", "update_own_profile", "delete_own_profile",
                "read_user_projects"
            ]

            for perm_name, perm_id in perm_name_map.items():
                role_permission_data.append(RolePermissionCreate(role_id=role_id_map["admin"], permission_id=perm_id))
                if perm_name in manager_permissions:
                    role_permission_data.append(RolePermissionCreate(role_id=role_id_map["manager"], permission_id=perm_id))
                if perm_name in employee_permissions:
                    role_permission_data.append(RolePermissionCreate(role_id=role_id_map["employee"], permission_id=perm_id))

            role_perm_repo = RolePermissionRepository(tenant_db)
            role_perm_repo.create_bulk(role_permission_data)

            # Step 7: Create user in tenant DB and assign Admin role
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

            # Step 8: Return created user
            return TenantUserOut.model_validate(user)

        finally:
            tenant_db.close()