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
    r"^/users$": {
        "GET": ["read_any_user"],
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
    r"^/comments$": {
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
    r"^/company-settings/?$": {
    "POST": ["create_company_settings"]
    },
    r"^/company-settings/\d+$": {
        "GET": ["read_company_settings"],
        "PUT": ["update_company_settings"],
        "DELETE": ["delete_company_settings"]
    },
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


