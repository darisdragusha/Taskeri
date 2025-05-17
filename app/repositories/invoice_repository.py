from sqlalchemy.orm import Session
from app.models.invoice import Invoice
from app.models.dtos.invoice_dtos import InvoiceCreate, InvoiceUpdate
from typing import List, Optional

class InvoiceRepository:
    """
    Repository for interacting with the Invoice table in the database.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: InvoiceCreate) -> Invoice:
        """
        Create a new invoice entry in the database.
        """
        invoice = Invoice(**data.model_dump())
        self.db.add(invoice)
        self.db.commit()
        self.db.refresh(invoice)
        return invoice

    def get_all(self) -> List[Invoice]:
        """
        Retrieve all invoices from the database.
        """
        return self.db.query(Invoice).all()

    def get_by_id(self, invoice_id: int) -> Optional[Invoice]:
        """
        Retrieve a specific invoice by its ID.
        """
        return self.db.query(Invoice).filter(Invoice.id == invoice_id).first()

    def update(self, invoice_id: int, data: InvoiceUpdate) -> Optional[Invoice]:
        """
        Update fields of an existing invoice.
        """
        invoice = self.get_by_id(invoice_id)
        if not invoice:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(invoice, key, value)
        self.db.commit()
        self.db.refresh(invoice)
        return invoice

    def delete(self, invoice_id: int) -> bool:
        """
        Delete an invoice by its ID.
        """
        invoice = self.get_by_id(invoice_id)
        if not invoice:
            return False
        self.db.delete(invoice)
        self.db.commit()
        return True
