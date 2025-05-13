from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from controllers.invoice_controller import InvoiceController
from models.dtos.invoice_dtos import InvoiceCreate, InvoiceUpdate, InvoiceResponse
from utils import get_db
from typing import List

router = APIRouter(prefix="/invoices", tags=["Invoices"])

def get_invoice_controller(db: Session = Depends(get_db)) -> InvoiceController:
    return InvoiceController(db)

@router.post("/", response_model=InvoiceResponse)
def create_invoice(
    data: InvoiceCreate,
    request: Request,
    controller: InvoiceController = Depends(get_invoice_controller)
):
    """
    Create a new invoice.

    Used by billing systems or company admins to log issued invoices for tracking and payments.

    - `company_id` must reference an existing company.
    - Status can be `"Pending"` or `"Paid"`.
    """
    return controller.create_invoice(data)

@router.get("/", response_model=List[InvoiceResponse])
def get_all_invoices(
    request: Request,
    controller: InvoiceController = Depends(get_invoice_controller)
):
    """
    Retrieve all invoices in the system.

    Useful for financial overviews, reporting, or administrative tools.
    """
    return controller.get_all_invoices()

@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(
    invoice_id: int,
    request: Request,
    controller: InvoiceController = Depends(get_invoice_controller)
):
    """
    Retrieve a single invoice by its ID.

    Returns 404 if the invoice is not found.
    """
    invoice = controller.get_invoice_by_id(invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.put("/{invoice_id}", response_model=InvoiceResponse)
def update_invoice(
    invoice_id: int,
    data: InvoiceUpdate,
    request: Request,
    controller: InvoiceController = Depends(get_invoice_controller)
):
    """
    Update an invoice's amount or status.

    - Only modifiable fields are `amount` and `status`.
    - Returns 404 if the invoice does not exist.
    """
    invoice = controller.update_invoice(invoice_id, data)
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.delete("/{invoice_id}", response_model=dict)
def delete_invoice(
    invoice_id: int,
    request: Request,
    controller: InvoiceController = Depends(get_invoice_controller)
):
    """
    Delete a specific invoice by its ID.

    Useful for cleanup or invoice invalidation. Irreversible.

    - Returns 404 if invoice is not found.
    """
    success = controller.delete_invoice(invoice_id)
    if not success:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"detail": "Invoice deleted"}
