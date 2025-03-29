from .test.login import router as loginRouter
from .test.protected_endpoint import router as protectedRouter

routers = [
    loginRouter,
    protectedRouter
]