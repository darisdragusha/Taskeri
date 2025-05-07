from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils import get_db
from controllers import TenantUserController
from models.dtos import TenantUserCreate, TenantUserOut

router = APIRouter(prefix="/tenant-users", tags=["Tenant Users"])

# Registration endpoint doesn't need permission check as it's a public endpoint
@router.post("/", response_model=TenantUserOut)
def register_user(
    user_data: TenantUserCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new tenant user. This is a public endpoint.
    """
    controller = TenantUserController(db)
    return controller.register_tenant_user(user_data)
