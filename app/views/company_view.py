from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from models.dtos import CompanyCreate, CompanyResponse, CompanyUpdate
from controllers import CompanyController
from utils import get_db
from typing import List

router = APIRouter(prefix="/companies", tags=["Companies"])

def get_company_controller(db: Session = Depends(get_db)) -> CompanyController:
    return CompanyController(db)

@router.post("/", response_model=CompanyResponse)
def create_company(
    data: CompanyCreate,
    request: Request,
    db: Session = Depends(get_db),
    controller: CompanyController = Depends(get_company_controller)
):
    """
    Create a new company. 
    
    Permission requirements (handled by middleware):
    - 'create_company' permission
    
    Business logic:
    - Only authorized administrators can create companies
    - Company names must be unique in the system
    """
    return controller.create_company(data)

@router.get("/", response_model=List[CompanyResponse])
def get_all_companies(
    request: Request,
    db: Session = Depends(get_db),
    controller: CompanyController = Depends(get_company_controller)
):
    """
    Get a list of all companies. 
    
    Permission requirements (handled by middleware):
    - 'read_company' permission
    
    Business logic:
    - Users with proper permissions can view all companies
    - Results may be filtered based on user access level in implementation
    """
    return controller.get_all_companies()

@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: int,
    request: Request,
    db: Session = Depends(get_db),
    controller: CompanyController = Depends(get_company_controller)
):
    """
    Get a specific company by ID. 
    
    Permission requirements (handled by middleware):
    - 'read_company' permission
    
    Business logic:
    - Users with proper permissions can view company details
    - Company must exist or a 404 error is returned
    """
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
    controller: CompanyController = Depends(get_company_controller)
):
    """
    Update a specific company by ID. 
    
    Permission requirements (handled by middleware):
    - 'update_company' permission
    
    Business logic:
    - Only authorized administrators can update company information
    - Company must exist or a 404 error is returned
    - Company name changes must not conflict with existing companies
    """
    company = controller.update_company(company_id, data)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.delete("/{company_id}", response_model=dict)
def delete_company(
    company_id: int,
    request: Request,
    db: Session = Depends(get_db),
    controller: CompanyController = Depends(get_company_controller)
):
    """
    Delete a specific company by ID. 
    
    Permission requirements (handled by middleware):
    - 'delete_company' permission
    
    Business logic:
    - Only authorized administrators can delete companies
    - Company must exist or a 404 error is returned
    - Deletion may be restricted if the company has associated departments, teams or users
    """
    success = controller.delete_company(company_id)
    if not success:
        raise HTTPException(status_code=404, detail="Company not found")
    return {"detail": "Company deleted"}