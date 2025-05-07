from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from models.dtos import CompanyCreate, CompanyResponse, CompanyUpdate
from controllers import CompanyController
from utils import get_db
from utils.permission_utils import PermissionChecker
from typing import List

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.post("/", response_model=CompanyResponse)
def create_company(
    data: CompanyCreate,
    request: Request,
    db: Session = Depends(get_db),
    user_data: dict = Depends(PermissionChecker.require_permission("create_company"))
):
    """
    Create a new company. Requires 'create_company' permission.
    """
    controller = CompanyController(db)
    return controller.create_company(data)

@router.get("/", response_model=List[CompanyResponse])
def get_all_companies(
    request: Request,
    db: Session = Depends(get_db),
    user_data: dict = Depends(PermissionChecker.require_permission("read_company"))
):
    """
    Get a list of all companies. Requires 'read_company' permission.
    """
    controller = CompanyController(db)
    return controller.get_all_companies()

@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user_data: dict = Depends(PermissionChecker.require_permission("read_company"))
):
    """
    Get a specific company by ID. Requires 'read_company' permission.
    """
    controller = CompanyController(db)
    company = controller.get_company_by_id(company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: int,
    data: CompanyUpdate,
    request: Request,
    db: Session = Depends(get_db),
    user_data: dict = Depends(PermissionChecker.require_permission("update_company"))
):
    """
    Update a specific company by ID. Requires 'update_company' permission.
    """
    controller = CompanyController(db)
    company = controller.update_company(company_id, data)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.delete("/{company_id}", response_model=dict)
def delete_company(
    company_id: int,
    request: Request,
    db: Session = Depends(get_db),
    user_data: dict = Depends(PermissionChecker.require_permission("delete_company"))
):
    """
    Delete a specific company by ID. Requires 'delete_company' permission.
    """
    controller = CompanyController(db)
    success = controller.delete_company(company_id)
    if not success:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"detail": "Company deleted"}