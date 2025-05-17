from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.controllers.company_settings_controller import CompanySettingsController
from app.models.dtos.company_settings_dtos import (
    CompanySettingsCreate,
    CompanySettingsUpdate,
    CompanySettingsResponse,
)
from app.utils import get_db
from app.auth import auth_service

router = APIRouter(prefix="/company-settings", tags=["Company Settings"])

def get_company_settings_controller(db: Session = Depends(get_db)) -> CompanySettingsController:
    return CompanySettingsController(db)

@router.post("/", response_model=CompanySettingsResponse)
def create_company_settings(
    data: CompanySettingsCreate,
    request: Request,
    controller: CompanySettingsController = Depends(get_company_settings_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Create settings for a specific company.
    """
    return controller.create_settings(data)

@router.get("/{company_id}", response_model=CompanySettingsResponse)
def get_company_settings(
    company_id: int,
    request: Request,
    controller: CompanySettingsController = Depends(get_company_settings_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Retrieve settings for a specific company.
    """
    settings = controller.get_settings(company_id)
    if not settings:
        raise HTTPException(status_code=404, detail="Company settings not found")
    return settings

@router.put("/{company_id}", response_model=CompanySettingsResponse)
def update_company_settings(
    company_id: int,
    data: CompanySettingsUpdate,
    request: Request,
    controller: CompanySettingsController = Depends(get_company_settings_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Update settings for a specific company.
    """
    updated = controller.update_settings(company_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Company settings not found")
    return updated

@router.delete("/{company_id}", response_model=dict)
def delete_company_settings(
    company_id: int,
    request: Request,
    controller: CompanySettingsController = Depends(get_company_settings_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Delete settings for a specific company.
    """
    deleted = controller.delete_settings(company_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Company settings not found")
    return {"detail": "Company settings deleted"}
