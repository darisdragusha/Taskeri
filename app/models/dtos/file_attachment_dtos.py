from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class FileAttachmentBase(BaseModel):
    task_id: int
    file_path: str = Field(..., max_length=255)

class FileAttachmentCreate(FileAttachmentBase):
    pass

class FileAttachmentUpdate(BaseModel):
    file_path: Optional[str] = Field(None, max_length=255)

class FileAttachmentResponse(FileAttachmentBase):
    id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True
