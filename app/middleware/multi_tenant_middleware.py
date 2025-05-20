from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from sqlalchemy.orm import Session
from typing import Awaitable, Callable
import logging

from app.auth import auth_service
from app.utils.db_utils import get_tenant_session, switch_schema, get_global_db

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
        public_paths = {
            "/login", "/register", "/docs", "/openapi.json", "/token", "/tenant-users/"
        }

        # Allow OPTIONS method (CORS preflight) and public routes
        if request.method == "OPTIONS" or request.url.path in public_paths:
            with get_global_db() as db:
                switch_schema(db, "taskeri_global")
                request.state.db = db
                response = await call_next(request)
                return response

        # Extract token
        token: str = await self.extract_token(request)

        try:
            # Verify token and extract user & tenant info
            user_data: dict = auth_service.verify_token(token)
            user_id: int = user_data["user_id"]
            tenant_id: int = user_data["tenant_id"]
            tenant_schema: str = user_data["tenant_name"]

            # Attach to request state
            request.state.user_id = user_id
            request.state.tenant_id = tenant_id
            request.state.tenant_schema = tenant_schema

            # Get tenant session and switch schema
            schema_name = f"tenant_{tenant_schema}"
            db: Session = get_tenant_session(schema_name)
            switch_schema(db, schema_name)
            request.state.db = db

            response: Response = await call_next(request)
            db.close()
            return response

        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error("Error in middleware dispatch", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error")

    async def extract_token(self, request: Request) -> str:
        """
        Extract the Bearer token from Authorization header.
        """
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            logger.error("Missing or invalid Authorization header.")
            raise HTTPException(status_code=401, detail="Missing or invalid token")
        return auth_header.split(" ")[1]