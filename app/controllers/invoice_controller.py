from sqlalchemy.orm import Session
from repositories.invoice_repository import InvoiceRepository
from models.dtos.invoice_dtos import InvoiceCreate, InvoiceUpdate
from models.invoice import Invoice
from typing import List, Optional

class InvoiceController:
    """
    Handles business logic related to invoice processing.
    """

    def __init__(self, db: Session):
        self.repo = InvoiceRepository(db)

    def create_invoice(self, data: InvoiceCreate) -> Invoice:
        """
        Create and return a new invoice.
        """
        return self.repo.create(data)

    def get_all_invoices(self) -> List[Invoice]:
        """
        Return all available invoices.
        """
        return self.repo.get_all()

    def get_invoice_by_id(self, invoice_id: int) -> Optional[Invoice]:
        """
        Return a specific invoice by ID.
        """
        return self.repo.get_by_id(invoice_id)

    def update_invoice(self, invoice_id: int, data: InvoiceUpdate) -> Optional[Invoice]:
        """
        Modify an existing invoice by ID.
        """
        return self.repo.update(invoice_id, data)

    def delete_invoice(self, invoice_id: int) -> bool:
        """
        Remove an invoice by its ID.
        """
        return self.repo.delete(invoice_id)
