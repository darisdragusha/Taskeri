from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.utils import get_db
from app.controllers import TenantUserController
from app.models.dtos import TenantUserCreate, TenantUserOut
from app.auth import auth_service

router = APIRouter(prefix="/tenant-users", tags=["Tenant Users"])

@router.post("/", response_model=TenantUserOut)
def register_user(
    user_data: TenantUserCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Register a new tenant user. 
    
    This is a public endpoint that doesn't require authentication or permissions.
    
    Business logic:
    - Creates a new user in the tenant_users table
    - Provisions a new tenant schema for the registered user
    - Sets up initial database structure for the new tenant
    - Ensures email address is unique across all tenants
    - Hashes the provided password for secure storage
    """
    controller = TenantUserController(db)
    return controller.register_tenant_user(user_data, request)
