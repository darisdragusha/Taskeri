from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.db_utils import get_db
from app.controllers.tenant_user_controller import TenantUserController
from app.models.dtos.tenant_user_dtos import TenantUserCreate, TenantUserOut

router = APIRouter(prefix="/tenant-users", tags=["Tenant Users"])

@router.post("/", response_model=TenantUserOut)
def register_user(
    user_data: TenantUserCreate,
    db: Session = Depends(get_db)
):
    controller = TenantUserController(db)
    return controller.register_tenant_user(user_data)  # ✅ returns a Pydantic model
