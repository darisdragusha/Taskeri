from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class InvoiceCreate(BaseModel):
    company_id: int
    amount: float
    status: Literal["Pending", "Paid"] = "Pending"

class InvoiceUpdate(BaseModel):
    amount: float | None = None
    status: Literal["Pending", "Paid"] | None = None

class InvoiceResponse(BaseModel):
    id: int
    company_id: int
    amount: float
    issued_at: datetime
    status: str

    class Config:
        orm_mode = True
