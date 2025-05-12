from .login_view import router as login_router 
from .user_view import router as user_router
from .task_view import router as task_router
from .role_view import router as role_router
from .permission_view import router as permission_router
from .company_view import router as company_router
from .user_role_view import router as user_role_router
from .tenant_user_view import router as tenant_user_router
from .project_views import router as project_router
from .team_view import router as team_router
from .department_view import router as department_router
from .comment_view import router as comment_router
from .user_profile_views import router as user_profile_router

routers = [
    login_router,
    user_router,
    task_router,
    role_router,
    permission_router,
    company_router,
    user_role_router,
    tenant_user_router,
    project_router, 
    team_router,
    department_router,
    comment_router,
    user_profile_router
]

