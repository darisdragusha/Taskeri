from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from sqlalchemy.orm import Session
from typing import Awaitable, Callable, Set
import logging
import json
from jose import JWTError

from app.auth import auth_service
from app.utils.db_utils import get_tenant_session, switch_schema, get_global_db
from app.config.routes_config import PUBLIC_ROUTES

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiTenantMiddleware(BaseHTTPMiddleware):
    """
    Middleware for handling multi-tenancy by extracting tenant-specific information from JWT tokens.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        Process incoming requests, verify authentication, and dynamically set the tenant schema.
        """
        # Public routes that don't require authentication
        public_paths = PUBLIC_ROUTES

        # Allow OPTIONS method (CORS preflight) and public routes
        if request.method == "OPTIONS" or any(request.url.path == route for route in public_paths):
            with get_global_db() as db:
                switch_schema(db, "taskeri_global")
                request.state.db = db
                response = await call_next(request)
                return response
        
        # Extract token
        try:
            token: str = await self.extract_token(request)
        except HTTPException as e:
            return Response(
                content=json.dumps({"detail": "Not authenticated"}),
                status_code=e.status_code,
                media_type="application/json"
            )

        try:
            # Verify token and extract user & tenant info
            user_data: dict = auth_service.verify_token(token)
            user_id: int = user_data.get("user_id")
            tenant_id: int = user_data.get("tenant_id") 
            tenant_name: str = user_data.get("tenant_name")

            if not all([user_id, tenant_id, tenant_name]):
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token format: missing required claims"
                )

            # Attach to request state
            request.state.user_id = user_id
            request.state.tenant_id = tenant_id
            request.state.tenant_schema = tenant_name

            # For test environment, use the provided test database
            if hasattr(request.state, "test_db"):
                db = request.state.test_db
                schema_name = f"tenant_{tenant_name}"
                try:
                    switch_schema(db, schema_name)
                except Exception as e:
                    logger.error(f"Error switching schema in test environment: {str(e)}")
                    # Attempt to restore a connection if it was closed
                    if "closed" in str(e).lower():
                        logger.info("Attempting to restore test database connection")
            else:
                # Get tenant session and switch schema for production
                schema_name = f"tenant_{tenant_name}"
                db = get_tenant_session(schema_name)
                switch_schema(db, schema_name)
            
            request.state.db = db

            # Process the request
            response = await call_next(request)

            # Close the DB session only if it's not a test session
            if not hasattr(request.state, "test_db"):
                try:
                    db.close()
                except Exception as e:
                    logger.error(f"Error closing database connection: {str(e)}")

            return response

        except JWTError:
            return Response(
                content=json.dumps({"detail": "Invalid or expired token"}),
                status_code=401,
                media_type="application/json"
            )
        except HTTPException as e:
            logger.error(f"HTTP error in middleware: {str(e)}")
            return Response(
                content=json.dumps({"detail": e.detail}),
                status_code=e.status_code,
                media_type="application/json"
            )
        except Exception as e:
            logger.error("Error in middleware dispatch", exc_info=True)
            return Response(
                content=json.dumps({"detail": "Internal server error"}),
                status_code=500,
                media_type="application/json"
            )

    async def extract_token(self, request: Request) -> str:
        """
        Extract the Bearer token from Authorization header.
        """
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.error("Missing or invalid Authorization header.")
            raise HTTPException(status_code=401, detail="Missing or invalid token")
        return auth_header.split(" ")[1]