from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy import text
from starlette.responses import Response
from typing import Awaitable, Callable, Dict, Any, List, Optional, Set
import logging
import re

# Setup basic logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthorizationMiddleware(BaseHTTPMiddleware):
    """
    Middleware for handling authorization in a centralized way.
    
    This middleware:
    - Checks if the requested endpoint requires authorization
    - Verifies user permissions against route requirements
    - Handles resource ownership checks
    - Efficiently caches permission checks for the duration of a request
    """
    
    def __init__(self, app, public_routes: List[str] = None, route_permissions: Dict[str, Dict] = None):
        """
        Initialize the AuthorizationMiddleware.
        
        Args:
            app: The FastAPI application
            public_routes: List of routes that don't require authentication
            route_permissions: Dictionary mapping route patterns to required permissions
        """
        super().__init__(app)
        self.public_routes = public_routes or []
        self.route_permissions = route_permissions or {}
        # Compile regex patterns for route matching
        self.compiled_patterns = {
            re.compile(pattern): permissions 
            for pattern, permissions in self.route_permissions.items()
        }
        
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        """
        Process incoming requests and verify authorization.
        
        Args:
            request (Request): The incoming FastAPI request
            call_next (Callable): The next middleware or endpoint handler
            
        Returns:
            Response: The response from the next middleware or endpoint
        """
        # Initialize a cache for permission checks in this request
        request.state.permission_cache = {}
        
        # Skip authorization for public routes
        path = request.url.path
        method = request.method
        
        if self._is_public_route(path):
            return await call_next(request)
            
        # Skip if no user is authenticated yet (handled by authentication middleware)
        if not hasattr(request.state, "user_id"):
            return await call_next(request)
            
        # Get user and tenant IDs from request state (set by auth middleware)
        user_id = request.state.user_id
        db = request.state.db
        
        # Check permissions for this route
        required_permissions = self._get_required_permissions(path, method)
        
        if required_permissions and not await self._check_permissions(db, user_id, required_permissions):
            # Check if this is a resource ownership route
            is_owner = await self._check_resource_ownership(request, path, user_id)
            if not is_owner:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You don't have permission to access this resource"
                )
        
        response = await call_next(request)
        return response
        
    def _is_public_route(self, path: str) -> bool:
        """Check if a route is public and doesn't require auth"""
        return any(path.startswith(route) for route in self.public_routes)
        
    def _get_required_permissions(self, path: str, method: str) -> List[str]:
        """Get the required permissions for a specific route and method"""
        for pattern, permissions in self.compiled_patterns.items():
            if pattern.match(path):
                # Get permissions for this HTTP method or use default
                return permissions.get(method, permissions.get("default", []))
        return []
        
    async def _check_permissions(
        self, db, user_id: int, permissions: List[str], require_all: bool = False
    ) -> bool:
        """
        Check if user has the required permissions.
        
        Args:
            db: Database session
            user_id: ID of the user
            permissions: List of permission names to check
            require_all: If True, require all permissions; otherwise, any one is sufficient
            
        Returns:
            bool: True if user has the required permissions
        """
        # Initialize permission cache in request.state if it doesn't exist
        if not hasattr(request.state, "permission_cache"):
            request.state.permission_cache = {}
        cache = request.state.permission_cache
        
        results = []
        for permission in permissions:
            # Check cache first
            cache_key = f"{user_id}:{permission}"
            if cache_key in cache:
                results.append(cache[cache_key])
                continue
                
            # If not in cache, check database
            query = text("""
                SELECT COUNT(*) > 0 
                FROM user_roles ur
                JOIN role_permissions rp ON ur.role_id = rp.role_id
                JOIN permissions p ON rp.permission_id = p.id
                WHERE ur.user_id = :user_id AND p.name = :permission_name
            """)
            
            result = db.execute(query, {"user_id": user_id, "permission_name": permission}).scalar()
            
            # Cache the result
            cache[cache_key] = result
            results.append(result)
        
        # Check if the user has the required permissions
        if require_all:
            return all(results)
        else:
            return any(results)
            
    async def _check_resource_ownership(self, request: Request, path: str, user_id: int) -> bool:
        """
        Check if user owns or can access a specific resource.
        
        Args:
            request: The request object
            path: The request path
            user_id: ID of the user
            
        Returns:
            bool: True if user owns or can access the resource
        """
        # Extract resource type and ID from the path
        # Example: /tasks/123 -> resource_type="task", resource_id=123
        path_parts = path.strip('/').split('/')
        if len(path_parts) < 2:
            return False
            
        resource_type = path_parts[0].rstrip('s')  # Convert plural to singular
        try:
            resource_id = int(path_parts[1])
        except (ValueError, IndexError):
            return False
            
        db = request.state.db
        
        # Check ownership based on resource type
        if resource_type == "task":
            query = text("""
                SELECT EXISTS (
                    SELECT 1 FROM tasks t
                    LEFT JOIN task_assignments ta ON t.id = ta.task_id
                    WHERE t.id = :resource_id AND (ta.user_id = :user_id OR EXISTS (
                        SELECT 1 FROM user_roles ur
                        JOIN roles r ON ur.role_id = r.id
                        WHERE ur.user_id = :user_id AND r.name IN ('Admin', 'Manager')
                    ))
                )
            """)
        elif resource_type == "project":
            query = text("""
                SELECT EXISTS (
                    SELECT 1 FROM projects p
                    WHERE p.id = :resource_id AND EXISTS (
                        SELECT 1 FROM user_roles ur
                        JOIN roles r ON ur.role_id = r.id
                        WHERE ur.user_id = :user_id AND r.name IN ('Admin', 'Manager')
                    )
                )
            """)
        elif resource_type == "user":
            # Special case for user resources - users can access their own profile
            return resource_id == user_id or await self._check_permissions(
                db, user_id, ["read_any_user"], False)
        else:
            # Default to admin check for unknown resource types
            query = text("""
                SELECT EXISTS (
                    SELECT 1 FROM user_roles ur
                    JOIN roles r ON ur.role_id = r.id
                    WHERE ur.user_id = :user_id AND r.name = 'Admin'
                )
            """)
            
        result = db.execute(query, {"resource_id": resource_id, "user_id": user_id}).scalar()
        return result