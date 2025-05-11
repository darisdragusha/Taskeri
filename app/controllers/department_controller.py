from sqlalchemy.orm import Session
from typing import List, Optional
from repositories import DepartmentRepository
from models.dtos import DepartmentCreate, DepartmentUpdate
from models.department import Department


class DepartmentController:
    """
    Controller for handling business logic related to departments.
    """

    def __init__(self, db: Session):
        self.repo = DepartmentRepository(db)

    def create_department(self, data: DepartmentCreate) -> Department:
        """
        Handle creation of a new department.
        """
        return self.repo.create_department(data.name, data.company_id)

    def get_all_departments(self) -> List[Department]:
        """
        Return a list of all departments.
        """
        return self.repo.get_all_departments()

    def get_department_by_id(self, department_id: int) -> Optional[Department]:
        """
        Return a department by its ID.
        """
        return self.repo.get_department_by_id(department_id)

    def update_department(self, department_id: int, data: DepartmentUpdate) -> Optional[Department]:
        """
        Update an existing department using its ID and new data.
        """
        return self.repo.update_department(department_id, data.dict(exclude_unset=True))

    def delete_department(self, department_id: int) -> bool:
        """
        Delete a department by its ID.
        """
        deleted = self.repo.delete_department(department_id)
        return deleted is not None
