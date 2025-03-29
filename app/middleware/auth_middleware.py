from fastapi import Request, HTTPException, Depends
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy import text
from starlette.responses import Response
from sqlalchemy.orm import Session
from utils.db_utils import SessionLocal
from auth.auth import auth_service
from typing import Awaitable, Callable, Dict, Any
import logging

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MultiTenantMiddleware(BaseHTTPMiddleware):
    """
    Middleware for handling multi-tenancy by extracting tenant-specific information from JWT tokens.

    This middleware:
    - Extracts the JWT token from the `Authorization` header.
    - Decodes and verifies the token to retrieve `user_id` and `tenant_id`.
    - Dynamically switches the database schema based on the `tenant_id`.
    - Attaches the authenticated user's information and the database session to the request state.
    """

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        Process incoming requests, verify authentication, and dynamically set the tenant schema.

        Args:
            request (Request): The incoming FastAPI request.
            call_next (Callable[[Request], Awaitable[Response]]): The next middleware or endpoint handler.

        Returns:
            Response: The response from the next middleware or endpoint.

        Raises:
            HTTPException: If the token is missing, invalid, or cannot be decoded.
        """
        # Exclude public routes from authentication
        if request.url.path in {"/login", "/register", "/docs","/openapi.json","/token"}:
            return await call_next(request)

        # Extract and verify the token
        token: str = await self.extract_token(request)

        try:
            # Decode the token to extract user and tenant details
            user_data: Dict[str, int | str] = auth_service.verify_token(token)
            user_id: int = user_data["user_id"]
            tenant_id: str = user_data["tenant_id"]

            # Attach extracted data to request state for later use in the request lifecycle
            request.state.user_id = user_id
            request.state.tenant_id = tenant_id

            # Initialize a new database session and set the tenant schema
            db: Session = SessionLocal()
            await self.set_session_schema(db, tenant_id)
            request.state.db = db

        except HTTPException as e:
            raise e  # Rethrow exception from `verify_token`

        response: Response = await call_next(request)
        return response

    async def extract_token(self, request: Request) -> str:
        """
        Extract and validate the JWT token from the request header.

        Args:
            request (Request): The FastAPI request object.

        Returns:
            str: The JWT token.

        Raises:
            HTTPException: If the token is missing or invalid.
        """
        auth_header: str | None = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid token")
        
        return auth_header.split(" ")[1]

    async def set_session_schema(self, db: Session, tenant_id: str) -> None:
        """
        Switch the active database schema dynamically based on the `tenant_id`.

        This function ensures that all queries for the request will operate within the correct tenant schema.

        Args:
            db (Session): The active SQLAlchemy database session.
            tenant_id (str): The tenant identifier used to determine the schema.

        Returns:
            None

        Raises:
            HTTPException: If the schema switching fails.
        """
        schema_name: str = f"tenant_{tenant_id}"

        try:
            # Use a single session to set the schema dynamically
            db.execute(text(f"USE {schema_name};"))
            db.commit()
            logger.info(f"Switched to schema: {schema_name}")
        except Exception as e:
            logger.error(f"Failed to switch schema {schema_name}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to switch tenant schema: {str(e)}")
