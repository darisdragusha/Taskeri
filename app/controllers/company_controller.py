from sqlalchemy.orm import Session
from repositories import CompanyRepository
from models.dtos import CompanyCreate, CompanyUpdate
from typing import List, Optional
from models.company import Company

class CompanyController:
    """
    Controller for handling business logic related to companies.
    """

    def __init__(self, db: Session):
        self.repo = CompanyRepository(db)

    def create_company(self, data: CompanyCreate) -> Company:
        """
        Handle creation of a new company.
        """
        return self.repo.create(data)

    def get_all_companies(self) -> List[Company]:
        """
        Return a list of all companies.
        """
        return self.repo.get_all()

    def get_company_by_id(self, company_id: int) -> Optional[Company]:
        """
        Return a company by its ID.
        """
        return self.repo.get_by_id(company_id)

    def update_company(self, company_id: int, data: CompanyUpdate) -> Optional[Company]:
        """
        Update an existing company using its ID and new data.
        """
        return self.repo.update(company_id, data)

    def delete_company(self, company_id: int) -> bool:
        """
        Delete a company by its ID.
        """
        return self.repo.delete(company_id)