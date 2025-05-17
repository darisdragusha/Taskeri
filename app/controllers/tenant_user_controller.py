from app.models.dtos import TenantUserCreate, TenantUserOut
from app.repositories import TenantUserRepository
from app.repositories.user_repository import UserRepository
from app.repositories.permission_repository import PermissionRepository
from app.repositories.role_repository import RoleRepository
from app.utils.db_utils import get_tenant_scoped_session
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

        create_new_tenant(self.repo.db, user_data.tenant_schema)
        user = self.repo.create(user_data)

        tenant_db = get_tenant_scoped_session("tenant_"+user_data.tenant_schema)

        PERMISSIONS = [
            # Company
            "read_company", "create_company", "update_company", "delete_company",

            # Role
            "read_role", "create_role", "update_role", "delete_role",

            # User
            "read_user", "read_any_user", "create_user", "update_user", "update_any_user",
            "delete_user",

            # User Role Management
            "manage_user_roles",

            # Tasks
            "read_task", "read_any_task", "read_any_user_task",
            "create_task", "update_task", "update_any_task",
            "delete_own_task", "delete_any_task",

            # Statistics
            "view_statistics",

            # Permissions
            "read_permission", "create_permission", "update_permission", "delete_permission",

            # Comments
            "create_comment", "read_comment", "update_comment", "delete_comment",

            # Attendance
            "check_in", "check_out", "read_own_attendance", "read_any_user_attendance",

            # Company Settings
            "create_company_settings", "read_company_settings", "update_company_settings", "delete_company_settings",

            # Departments
            "read_department", "create_department", "update_department", "delete_department",

            # File Attachments
            "read_attachment", "create_attachment", "update_attachment", "delete_attachment",

            # Invoices
            "read_invoice", "create_invoice", "update_invoice", "delete_invoice",

            # Leave Requests
            "create_leave_request", "read_leave_request", "update_leave_status",
            "delete_leave_request", "read_any_user_leave_request",

            # Projects
            "read_project", "create_project", "update_project", "update_any_project",
            "delete_project", "delete_any_project",

            # Role Permissions
            "manage_role_permissions",

            # Teams
            "read_team", "create_team", "update_team", "delete_team",

            # Time Logs
            "create_time_log", "read_time_log", "read_own_time_log", "read_user_time_log",
            "update_time_log", "update_own_time_log", "delete_time_log", "delete_own_time_log",

            # User Profiles
            "create_user_profile", "read_own_profile", "read_any_profile",
            "update_own_profile", "update_any_profile",
            "delete_own_profile", "delete_any_profile",

            # Project-User Assignments
            "assign_user_to_project", "remove_user_from_project",
            "read_project_users", "read_user_projects"
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

        manager_permissions = [
        # Company
        "read_company",

        # Role
        "read_role",

        # User
        "read_user", "read_any_user", "update_user",

        # Tasks
        "read_task", "read_any_task", "read_any_user_task",
        "create_task", "update_task", "update_any_task", "delete_own_task",

        # Comments
        "read_comment", "create_comment", "update_comment", "delete_comment",

        # Attendance
        "read_any_user_attendance",

        # Departments
        "read_department", "create_department", "update_department", "delete_department",

        # Attachments
        "read_attachment",

        # Leave Requests
        "read_leave_request", "update_leave_status", "read_any_user_leave_request",

        # Projects
        "read_project", "create_project", "update_project", "update_any_project", "delete_project",

        # Teams
        "read_team", "create_team", "update_team", "delete_team",

        # Time Logs
        "read_time_log", "read_user_time_log",

        # User Profiles
        "read_any_profile", "update_any_profile",

        # Project-User
        "assign_user_to_project", "remove_user_from_project", "read_project_users", "read_user_projects",

        # Stats
        "view_statistics"
    ]
        

        employee_permissions = [
        # Tasks
        "read_task", "create_task", "update_task", "delete_own_task",

        # Comments
        "read_comment", "create_comment", "update_comment",

        # Attendance
        "check_in", "check_out", "read_own_attendance",

        # Leave Requests
        "create_leave_request", "read_leave_request", "delete_leave_request",

        # Time Logs
        "create_time_log", "read_own_time_log", "update_own_time_log", "delete_own_time_log",

        # User Profiles
        "create_user_profile", "read_own_profile", "update_own_profile", "delete_own_profile",

        # Projects
        "read_user_projects"
    ]
        
        #Default Roles Assigned Permissions

        for perm_name, perm_id in perm_name_map.items():
            # Admin gets everything
            role_permission_data.append(RolePermissionCreate(role_id=role_id_map["admin"], permission_id=perm_id))

            # Manager
            if perm_name in manager_permissions:
                role_permission_data.append(RolePermissionCreate(role_id=role_id_map["manager"], permission_id=perm_id))

            # Employee
            if perm_name in employee_permissions:
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
