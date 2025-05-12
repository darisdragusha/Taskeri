from sqlalchemy.orm import Session
from repositories.company_settings_repository import CompanySettingsRepository
from models.dtos.company_settings_dtos import CompanySettingsCreate, CompanySettingsUpdate
from models.company_settings import CompanySettings
from typing import Optional

class CompanySettingsController:
    """
    Controller for handling business logic around company settings.
    """

    def __init__(self, db: Session):
        self.repo = CompanySettingsRepository(db)

    def create_settings(self, data: CompanySettingsCreate) -> CompanySettings:
        """
        Create new settings for a company.
        """
        return self.repo.create(data)

    def get_settings(self, company_id: int) -> Optional[CompanySettings]:
        """
        Get settings for a specific company.
        """
        return self.repo.get_by_company_id(company_id)

    def update_settings(self, company_id: int, data: CompanySettingsUpdate) -> Optional[CompanySettings]:
        """
        Update settings for a specific company.
        """
        return self.repo.update(company_id, data)

    def delete_settings(self, company_id: int) -> bool:
        """
        Delete settings for a specific company.
        """
        return self.repo.delete(company_id)
