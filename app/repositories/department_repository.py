from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List, Dict, Any
from app.models.department import Department

class DepartmentRepository:
    """Repository for managing department-related database operations."""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_department(self, name: str, company_id: int) -> Department:
        """
        Create a new department.

        Args:
            name (str): Department name.
            company_id (int): ID of the company the department belongs to.

        Returns:
            Department: Newly created department instance.
        """
        try:
            department = Department(name=name, company_id=company_id)
            self.db_session.add(department)
            self.db_session.commit()
            self.db_session.refresh(department)
            return department
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_department_by_id(self, department_id: int) -> Optional[Department]:
        """Retrieve a department by its ID."""
        return self.db_session.query(Department).filter(Department.id == department_id).first()

    def get_all_departments(self) -> List[Department]:
        """Retrieve all departments."""
        return self.db_session.query(Department).all()

    def update_department(self, department_id: int, update_data: Dict[str, Any]) -> Optional[Department]:
        """
        Update an existing department.

        Args:
            department_id (int): ID of the department to update.
            update_data (Dict[str, Any]): Fields and their new values.

        Returns:
            Optional[Department]: Updated department or None if not found.
        """
        try:
            department = self.get_department_by_id(department_id)
            if not department:
                return None

            for key, value in update_data.items():
                if hasattr(department, key) and value is not None:
                    setattr(department, key, value)

            self.db_session.commit()
            self.db_session.refresh(department)
            return department
        except Exception as e:
            self.db_session.rollback()
            raise e

    def delete_department(self, department_id: int) -> Optional[Department]:
        """
        Delete a department by ID.

        Returns:
            Optional[Department]: The deleted department or None if not found.
        """
        try:
            department = self.get_department_by_id(department_id)
            if department:
                self.db_session.delete(department)
                self.db_session.commit()
                return department
            return None
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_department_statistics(self) -> Dict[int, int]:
        """
        Generate statistics of departments grouped by company ID.

        Returns:
            Dict[int, int]: Dictionary where keys are company IDs and values are department counts.
        """
        results = (
            self.db_session.query(Department.company_id, func.count(Department.id))
            .group_by(Department.company_id)
            .all()
        )
        return {company_id: count for company_id, count in results}
