from .login_view import router as login_router 
from .user_view import router as user_router
from .task_view import router as task_router

routers = [
    login_router,
    user_router,
    task_router
]

