from sqlalchemy.orm import Session
from repositories.file_attachment_repository import FileAttachmentRepository
from models.dtos import FileAttachmentCreate, FileAttachmentUpdate
from models.file_attachment import FileAttachment
from typing import List, Optional

class FileAttachmentController:
    """
    Controller for handling file attachment logic.
    """

    def __init__(self, db: Session):
        self.repo = FileAttachmentRepository(db)

    def create_attachment(self, data: FileAttachmentCreate) -> FileAttachment:
        """
        Create a new file attachment.
        """
        return self.repo.create(data)

    def get_all_attachments(self) -> List[FileAttachment]:
        """
        Retrieve all file attachments.
        """
        return self.repo.get_all()

    def get_attachment_by_id(self, attachment_id: int) -> Optional[FileAttachment]:
        """
        Retrieve a file attachment by ID.
        """
        return self.repo.get_by_id(attachment_id)

    def get_attachments_by_task(self, task_id: int) -> List[FileAttachment]:
        """
        Retrieve file attachments by task ID.
        """
        return self.repo.get_by_task_id(task_id)

    def update_attachment(self, attachment_id: int, data: FileAttachmentUpdate) -> Optional[FileAttachment]:
        """
        Update a file attachment.
        """
        return self.repo.update(attachment_id, data)

    def delete_attachment(self, attachment_id: int) -> bool:
        """
        Delete a file attachment.
        """
        return self.repo.delete(attachment_id)
