from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.dtos.company_dtos import CompanyCreate, CompanyResponse, CompanyUpdate
from controllers.company_controller import CompanyController
from utils.db_utils import get_db
from auth import auth_service  # Import authentication dependency
from typing import List

router = APIRouter(prefix="/companies", tags=["Companies"])

@router.post("/", response_model=CompanyResponse)
def create_company(
    data: CompanyCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Create a new company. Requires authentication.
    """
    controller = CompanyController(db)
    return controller.create_company(data)

@router.get("/", response_model=List[CompanyResponse])
def get_all_companies(
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get a list of all companies. Requires authentication.
    """
    controller = CompanyController(db)
    return controller.get_all_companies()

@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get a specific company by ID. Requires authentication.
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
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Update a specific company by ID. Requires authentication.
    """
    controller = CompanyController(db)
    company = controller.update_company(company_id, data)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.delete("/{company_id}", response_model=dict)
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Delete a specific company by ID. Requires authentication.
    """
    controller = CompanyController(db)
    success = controller.delete_company(company_id)
    if not success:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"detail": "Company deleted"}