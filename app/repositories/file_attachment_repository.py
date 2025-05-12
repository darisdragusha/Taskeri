from sqlalchemy.orm import Session
from models.file_attachment import FileAttachment
from models.dtos import FileAttachmentCreate, FileAttachmentUpdate
from typing import List, Optional

class FileAttachmentRepository:
    """
    Repository for managing file attachments in the database.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: FileAttachmentCreate) -> FileAttachment:
        """
        Create a new file attachment record.
        """
        attachment = FileAttachment(**data.model_dump())
        self.db.add(attachment)
        self.db.commit()
        self.db.refresh(attachment)
        return attachment

    def get_all(self) -> List[FileAttachment]:
        """
        Retrieve all file attachments.
        """
        return self.db.query(FileAttachment).all()

    def get_by_id(self, attachment_id: int) -> Optional[FileAttachment]:
        """
        Retrieve a file attachment by its ID.
        """
        return self.db.query(FileAttachment).filter_by(id=attachment_id).first()

    def get_by_task_id(self, task_id: int) -> List[FileAttachment]:
        """
        Retrieve all file attachments for a given task.
        """
        return self.db.query(FileAttachment).filter_by(task_id=task_id).all()

    def update(self, attachment_id: int, data: FileAttachmentUpdate) -> Optional[FileAttachment]:
        """
        Update a file attachment by its ID.
        """
        attachment = self.get_by_id(attachment_id)
        if not attachment:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(attachment, key, value)
        self.db.commit()
        self.db.refresh(attachment)
        return attachment

    def delete(self, attachment_id: int) -> bool:
        """
        Delete a file attachment by its ID.
        """
        attachment = self.get_by_id(attachment_id)
        if not attachment:
            return False
        self.db.delete(attachment)
        self.db.commit()
        return True
