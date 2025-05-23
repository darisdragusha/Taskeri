from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from app.views import routers
from app.middleware import MultiTenantMiddleware, AuthorizationMiddleware 
from app.config.routes_config import PUBLIC_ROUTES, ROUTE_PERMISSIONS

# Function to set up routes
def setup_routes(app_instance):
    # Include routers
    for router in routers:
        app_instance.include_router(router)

# Function to set up middleware
def setup_middlewares(app_instance):
    # Add AuthorizationMiddleware after authentication (handles permissions)
    app_instance.add_middleware(
        AuthorizationMiddleware,
        public_routes=PUBLIC_ROUTES,
        route_permissions=ROUTE_PERMISSIONS
    )

    # Add MultiTenantMiddleware first (handles authentication)
    app_instance.add_middleware(MultiTenantMiddleware)

# Function to set up CORS
def setup_cors(app_instance):
    # CORS Configuration
    allowed_origins = ["http://localhost:3000", "https://taskeri-frontend.vercel.app"]


    
    app_instance.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
        allow_headers=["Authorization", "Content-Type", "Accept"],  
        expose_headers=["*"],
        max_age=3600,
    )

# Create the main app
app = FastAPI()

# Set up the app components
setup_cors(app)
setup_middlewares(app)
setup_routes(app)


