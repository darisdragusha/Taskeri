from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from utils.db_utils import SessionLocal
from auth.auth import auth_service  

class MultiTenantMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Exclude public routes
        if request.url.path in ["/login", "/register", "/docs"]:
            return await call_next(request)

        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid token")

        token = auth_header.split(" ")[1]

        try:
            user_data = auth_service.verify_token(token)
            user_id = user_data["user_id"]
            tenant_id = user_data["tenant_id"]

            # Attach user & tenant info to request state
            request.state.user_id = user_id
            request.state.tenant_id = tenant_id

            # Set tenant schema dynamically
            db = SessionLocal()
            self.set_session_schema(db, tenant_id)
            request.state.db = db

        except HTTPException as e:
            raise e  # Rethrow exception from `verify_token`

        response = await call_next(request)
        db.close()  # Close DB session
        return response

    def set_session_schema(self, db: Session, tenant_id: str):
        """Set the tenant-specific schema dynamically."""
        schema_name = f"tenant_{tenant_id}"
        db.execute(f"USE {schema_name};")
        db.commit()
