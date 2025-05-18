from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.views import routers
from app.middleware import MultiTenantMiddleware, AuthorizationMiddleware 

app = FastAPI()

# CORS Configuration
allowed_origins = ["http://localhost", "http://127.0.0.1:8000", '*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define public routes that don't require authentication
PUBLIC_ROUTES = [
    "/login", 
    "/register", 
    "/docs", 
    "/openapi.json", 
    "/token", 
    "/tenant-users/"
]

# Define route permissions mapping - regexes are used for pattern matching
ROUTE_PERMISSIONS = {
    # Company routes
    r"^/companies/?$": {
        "GET": ["read_company"],
        "POST": ["create_company"]
    },
    r"^/companies/\d+$": {
        "GET": ["read_company"],
        "PUT": ["update_company"],
        "DELETE": ["delete_company"]
    },
    
    # Role routes
    r"^/roles$": {
        "GET": ["read_role"],
        "POST": ["create_role"]
    },
    r"^/roles/\d+$": {
        "GET": ["read_role"],
        "PUT": ["update_role"],
        "DELETE": ["delete_role"]
    },
    
    # User routes - can use either self-permission or any-permission
    r"^/users/?$": {
        "GET": ["read_any_user"],
    },
    r"^/users/create$": {
        "POST": ["create_user"]
    },
    r"^/users/\d+$": {
        "GET": ["read_user", "read_any_user"],
        "PUT": ["update_user", "update_any_user"],
        "DELETE": ["delete_user"]
    },
    
    # User role routes
    r"^/user-roles/\d+/roles$": {
        "GET": ["manage_user_roles"],
    },
    r"^/user-roles/\d+/roles/\d+$": {
        "POST": ["manage_user_roles"],
        "DELETE": ["manage_user_roles"]
    },
    
    # Task routes
    r"^/tasks$": {
        "GET": ["read_task"],
        "POST": ["create_task"]
    },
    r"^/tasks/\d+$": {
        "GET": ["read_task", "read_any_task"],
        "PUT": ["update_task", "update_any_task"],
        "DELETE": ["delete_own_task", "delete_any_task"]
    },
    r"^/tasks/\d+/details$": {
        "GET": ["read_task", "read_any_task"]
    },
    r"^/tasks/project/\d+$": {
        "GET": ["read_task"]
    },
    r"^/tasks/user/\d+$": {
        "GET": ["read_task", "read_any_user_task"]
    },
    r"^/tasks/statistics$": {
        "GET": ["view_statistics"]
    },
    
    # Permission routes
    r"^/permissions$": {
        "GET": ["read_permission"],
        "POST": ["create_permission"]
    },
    r"^/permissions/\d+$": {
        "GET": ["read_permission"],
        "PUT": ["update_permission"],
        "DELETE": ["delete_permission"]
    },
    
    # Comment routes
    r"^/comments/$": {
        "POST": ["create_comment"]
    },
    r"^/comments/\d+$": {
        "GET": ["read_comment"],
        "PUT": ["update_comment"],
        "DELETE": ["delete_comment"]
    },
    r"^/comments/task/\d+$": {
        "GET": ["read_comment"]
    },

    #Attendance routes
    r"^/attendance/check-in$": {
    "POST": ["check_in"]
    },
    r"^/attendance/check-out$": {
        "PUT": ["check_out"]
    },
    r"^/attendance/my$": {
        "GET": ["read_own_attendance"]
    },
    r"^/attendance/user/\d+$": {
        "GET": ["read_any_user_attendance"]
    },

    #Company Settings routes
    r"^/company-settings/?$": {
    "POST": ["create_company_settings"]
    },
    r"^/company-settings/\d+$": {
        "GET": ["read_company_settings"],
        "PUT": ["update_company_settings"],
        "DELETE": ["delete_company_settings"]
    },

    #Departments routes
    r"^/departments/?$": {
    "GET": ["read_department"],
    "POST": ["create_department"]
    },
    r"^/departments/\d+$": {
        "GET": ["read_department"],
        "PUT": ["update_department"],
        "DELETE": ["delete_department"]
    },

    # File Attachment routes
    r"^/attachments/?$": {
        "GET": ["read_attachment"],
        "POST": ["create_attachment"]
    },
    r"^/attachments/\d+$": {
        "GET": ["read_attachment"],
        "PUT": ["update_attachment"],
        "DELETE": ["delete_attachment"]
    },
    r"^/attachments/task/\d+$": {
        "GET": ["read_attachment"]
    },

    # Invoice routes
    r"^/invoices/?$": {
        "GET": ["read_invoice"],
        "POST": ["create_invoice"]
    },
    r"^/invoices/\d+$": {
        "GET": ["read_invoice"],
        "PUT": ["update_invoice"],
        "DELETE": ["delete_invoice"]
    },

    # Leave request routes
    r"^/leave-requests/?$": {
        "POST": ["create_leave_request"]
    },
    r"^/leave-requests/\d+$": {
        "GET": ["read_leave_request"],
        "DELETE": ["delete_leave_request"]
    },
    r"^/leave-requests/\d+/status$": {
        "PATCH": ["update_leave_status"]
    },
    r"^/leave-requests/user/\d+$": {
        "GET": ["read_any_user_leave_request"]
    },

    # Project routes
    r"^/projects/?$": {
        "GET": ["read_project"],
        "POST": ["create_project"]
    },
    r"^/projects/statistics$": {
        "GET": ["view_statistics"]
    },
    r"^/projects/\d+$": {
        "GET": ["read_project"],
        "PUT": ["update_project", "update_any_project"],
        "DELETE": ["delete_project", "delete_any_project"]
    },

    # Role-Permission routes
    r"^/role-permissions/?$": {
        "GET": ["manage_role_permissions"],
        "POST": ["manage_role_permissions"],
        "DELETE": ["manage_role_permissions"]
    },

    # Team routes
    r"^/teams/?$": {
        "GET": ["read_team"],
        "POST": ["create_team"]
    },
    r"^/teams/statistics$": {
        "GET": ["view_statistics"]
    },
    r"^/teams/\d+$": {
        "GET": ["read_team"],
        "PUT": ["update_team"],
        "DELETE": ["delete_team"]
    },

    # Time log routes
    r"^/time-logs/?$": {
        "POST": ["create_time_log"]
    },
    r"^/time-logs/my$": {
        "GET": ["read_own_time_log"]
    },
    r"^/time-logs/\d+$": {
        "GET": ["read_time_log", "read_own_time_log"],
        "PUT": ["update_time_log", "update_own_time_log"],
        "DELETE": ["delete_time_log", "delete_own_time_log"]
    },
    r"^/time-logs/task/\d+$": {
        "GET": ["read_time_log"]
    },
    r"^/time-logs/user/\d+/by-time$": {
        "GET": ["read_time_log", "read_user_time_log"]
    },

    # User Profile routes
    r"^/profiles/?$": {
        "POST": ["create_user_profile"]
    },
    r"^/profiles/\d+$": {
        "GET": ["read_own_profile", "read_any_profile"],
        "PUT": ["update_own_profile", "update_any_profile"],
        "DELETE": ["delete_own_profile", "delete_any_profile"]
    },

    # User role management routes
    r"^/user-roles/\d+/roles$": {
        "GET": ["manage_user_roles"]
    },
    r"^/user-roles/\d+/roles/\d+$": {
        "POST": ["manage_user_roles"],
        "DELETE": ["manage_user_roles"]
    },

    # Project-User assignment routes
    r"^/project-users/?$": {
        "POST": ["assign_user_to_project"],
        "DELETE": ["remove_user_from_project"]
    },
    r"^/project-users/\d+/users$": {
        "GET": ["read_project_users"]
    },
    r"^/project-users/users/\d+/projects$": {
        "GET": ["read_user_projects"]
    },
    r"^/project-users/me/projects$": {
        "GET": ["read_user_projects"]
    }
}


# Add AuthorizationMiddleware after authentication (handles permissions)
app.add_middleware(
    AuthorizationMiddleware,
    public_routes=PUBLIC_ROUTES,
    route_permissions=ROUTE_PERMISSIONS
)

# Add MultiTenantMiddleware first (handles authentication)

app.add_middleware(MultiTenantMiddleware)


# Include routers
for router in routers:
    app.include_router(router)


