from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from controllers.file_attachment_controller import FileAttachmentController
from models.dtos.file_attachment_dtos import (
    FileAttachmentCreate,
    FileAttachmentUpdate,
    FileAttachmentResponse
)
from utils import get_db
from typing import List
from auth import auth_service

router = APIRouter(prefix="/attachments", tags=["File Attachments"])

def get_file_attachment_controller(db: Session = Depends(get_db)) -> FileAttachmentController:
    return FileAttachmentController(db)

@router.post("/", response_model=FileAttachmentResponse)
def create_file_attachment(
    data: FileAttachmentCreate,
    request: Request,
    controller: FileAttachmentController = Depends(get_file_attachment_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Create a new file attachment.

    This endpoint allows clients to attach a file to a task by specifying the task ID and file path.
    The `uploaded_at` field is automatically set by the database.
    """
    return controller.create_attachment(data)

@router.get("/", response_model=List[FileAttachmentResponse])
def get_all_attachments(
    request: Request,
    controller: FileAttachmentController = Depends(get_file_attachment_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Retrieve all file attachments.

    Returns a list of all file attachments across tasks. 
    Useful for admins or analytics tools needing to inspect uploads.
    """
    return controller.get_all_attachments()

@router.get("/task/{task_id}", response_model=List[FileAttachmentResponse])
def get_attachments_by_task(
    task_id: int,
    request: Request,
    controller: FileAttachmentController = Depends(get_file_attachment_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get all attachments for a specific task.

    Use this to fetch every file associated with a particular task ID.
    """
    return controller.get_attachments_by_task(task_id)

@router.get("/{attachment_id}", response_model=FileAttachmentResponse)
def get_attachment_by_id(
    attachment_id: int,
    request: Request,
    controller: FileAttachmentController = Depends(get_file_attachment_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Retrieve a file attachment by ID.

    Returns detailed information about a specific file attachment.
    Raises 404 if not found.
    """
    attachment = controller.get_attachment_by_id(attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return attachment

@router.put("/{attachment_id}", response_model=FileAttachmentResponse)
def update_attachment(
    attachment_id: int,
    data: FileAttachmentUpdate,
    request: Request,
    controller: FileAttachmentController = Depends(get_file_attachment_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Update an existing file attachment.

    Currently supports updating only the file path. 
    Raises 404 if the attachment does not exist.
    """
    updated = controller.update_attachment(attachment_id, data)
    if not updated:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return updated

@router.delete("/{attachment_id}", response_model=dict)
def delete_attachment(
    attachment_id: int,
    request: Request,
    controller: FileAttachmentController = Depends(get_file_attachment_controller),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Delete a file attachment by ID.

    Permanently removes the record from the database.
    Returns a confirmation message or 404 if not found.
    """
    deleted = controller.delete_attachment(attachment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Attachment not found")
    return {"detail": "Attachment deleted"}
