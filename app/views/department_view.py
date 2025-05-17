from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.models.dtos.department_dtos import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from app.controllers.department_controller import DepartmentController
from app.utils import get_db
from typing import List
from app.auth import auth_service

router = APIRouter(prefix="/departments", tags=["Departments"])

def get_department_controller(db: Session = Depends(get_db)) -> DepartmentController:
    return DepartmentController(db)

@router.post("/", response_model=DepartmentResponse)
def create_department(
    data: DepartmentCreate,
    request: Request,
    db: Session = Depends(get_db),
    controller: DepartmentController = Depends(get_department_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Create a new department.

    Permission requirements (handled by middleware):
    - 'create_department' permission

    Business logic:
    - Only authorized administrators can create departments
    - Department names should be unique per company (enforced in business logic or DB)
    - The company must exist before creating a department
    """
    return controller.create_department(data)

@router.get("/", response_model=List[DepartmentResponse])
def get_all_departments(
    request: Request,
    db: Session = Depends(get_db),
    controller: DepartmentController = Depends(get_department_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get a list of all departments.

    Permission requirements (handled by middleware):
    - 'read_department' permission

    Business logic:
    - Users with appropriate permissions can view departments
    - Results may be filtered based on user's role or company
    """
    return controller.get_all_departments()

@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(
    department_id: int,
    request: Request,
    db: Session = Depends(get_db),
    controller: DepartmentController = Depends(get_department_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get a specific department by ID.

    Permission requirements (handled by middleware):
    - 'read_department' permission

    Business logic:
    - Department must exist or a 404 error is returned
    """
    department = controller.get_department_by_id(department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(
    department_id: int,
    data: DepartmentUpdate,
    request: Request,
    db: Session = Depends(get_db),
    controller: DepartmentController = Depends(get_department_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Update a specific department by ID.

    Permission requirements (handled by middleware):
    - 'update_department' permission

    Business logic:
    - Department must exist or a 404 error is returned
    - Updated name should not conflict with other departments within the same company
    """
    department = controller.update_department(department_id, data)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department

@router.delete("/{department_id}", response_model=dict)
def delete_department(
    department_id: int,
    request: Request,
    db: Session = Depends(get_db),
    controller: DepartmentController = Depends(get_department_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Delete a specific department by ID.

    Permission requirements (handled by middleware):
    - 'delete_department' permission

    Business logic:
    - Department must exist or a 404 error is returned
    - Deletion may be restricted if the department has associated teams or users
    """
    success = controller.delete_department(department_id)
    if not success:
        raise HTTPException(status_code=404, detail="Department not found")
    return {"detail": "Department deleted"}