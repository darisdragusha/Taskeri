from app.routers.tenant_user_router import router as tenant_user_router

routers = [
    tenant_user_router
]
from .test.login import router as loginRouter
from .test.protected_endpoint import router as protectedRouter

routers = [
    loginRouter,
    protectedRouter
]
