from .login_view import router as login_router 
from .user_view import router as user_router
from .tenant_user_view import router as tenant_user_router

routers = [
    login_router,
    tenant_user_router,
    user_router
]

