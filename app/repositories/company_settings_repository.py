from sqlalchemy.orm import Session
from app.models.company_settings import CompanySettings
from app.models.dtos.company_settings_dtos import CompanySettingsCreate, CompanySettingsUpdate
from typing import Optional

class CompanySettingsRepository:
    """
    Repository for managing company settings in the database.
    """

    def __init__(self, db: Session):
        """
        Initialize with DB session.
        """
        self.db = db

    def create(self, data: CompanySettingsCreate) -> CompanySettings:
        """
        Create settings for a company.

        :param data: CompanySettingsCreate DTO
        :return: Created CompanySettings instance
        """
        settings = CompanySettings(**data.model_dump())
        self.db.add(settings)
        self.db.commit()
        self.db.refresh(settings)
        return settings

    def get_by_company_id(self, company_id: int) -> Optional[CompanySettings]:
        """
        Get settings for a specific company.

        :param company_id: ID of the company
        :return: CompanySettings instance or None
        """
        return self.db.query(CompanySettings).filter_by(company_id=company_id).first()

    def update(self, company_id: int, data: CompanySettingsUpdate) -> Optional[CompanySettings]:
        """
        Update settings for a specific company.

        :param company_id: ID of the company
        :param data: CompanySettingsUpdate DTO
        :return: Updated CompanySettings instance or None
        """
        settings = self.get_by_company_id(company_id)
        if not settings:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(settings, key, value)
        self.db.commit()
        self.db.refresh(settings)
        return settings

    def delete(self, company_id: int) -> bool:
        """
        Delete settings for a specific company.

        :param company_id: ID of the company
        :return: True if deleted, False if not found
        """
        settings = self.get_by_company_id(company_id)
        if not settings:
            return False
        self.db.delete(settings)
        self.db.commit()
        return True