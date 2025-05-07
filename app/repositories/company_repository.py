from sqlalchemy.orm import Session
from models.company import Company
from models.dtos.company_dtos import CompanyCreate, CompanyUpdate
from typing import List, Optional

class CompanyRepository:
    """
    Repository class for handling database operations related to Company.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: CompanyCreate) -> Company:
        """
        Create a new company record in the database.
        """
        company = Company(**data.model_dump())
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company

    def get_all(self) -> List[Company]:
        """
        Retrieve all company records from the database.
        """
        return self.db.query(Company).all()

    def get_by_id(self, company_id: int) -> Optional[Company]:
        """
        Retrieve a single company by its ID.
        """
        return self.db.query(Company).filter(Company.id == company_id).first()

    def update(self, company_id: int, data: CompanyUpdate) -> Optional[Company]:
        """
        Update an existing company record by its ID.
        """
        company = self.get_by_id(company_id)
        if not company:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(company, key, value)
        self.db.commit()
        self.db.refresh(company)
        return company

    def delete(self, company_id: int) -> bool:
        """
        Delete a company record by its ID.
        """
        company = self.get_by_id(company_id)
        if not company:
            return False
        self.db.delete(company)
        self.db.commit()
        return True