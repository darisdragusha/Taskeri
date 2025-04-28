from pydantic import BaseModel, validator, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum

class PriorityEnum(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class StatusEnum(str, Enum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    TECHNICAL_REVIEW = "Technical Review"
    DONE = "Done"

class TaskBase(BaseModel):
    name: str
    project_id: int
    description: Optional[str] = None
    priority: PriorityEnum = PriorityEnum.MEDIUM
    status: StatusEnum = StatusEnum.TODO
    due_date: Optional[date] = None

class TaskCreate(TaskBase):
    assigned_user_ids: Optional[List[int]] = None

class TaskUpdate(BaseModel):
    name: Optional[str] = None
    project_id: Optional[int] = None
    description: Optional[str] = None
    priority: Optional[PriorityEnum] = None
    status: Optional[StatusEnum] = None
    due_date: Optional[date] = None
    assigned_user_ids: Optional[List[int]] = None

class UserBasicInfo(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True
        from_attributes = True

class CommentResponse(BaseModel):
    id: int
    content: str
    user_id: int
    created_at: str
    user: Optional[UserBasicInfo] = None

    class Config:
        orm_mode = True
        from_attributes = True

    @validator('created_at', pre=True)
    def datetime_to_str(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v

class FileAttachmentResponse(BaseModel):
    id: int
    file_path: str
    uploaded_at: str

    class Config:
        orm_mode = True
        from_attributes = True

    @validator('uploaded_at', pre=True)
    def datetime_to_str(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v

class ProjectBasicInfo(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        from_attributes = True

class TaskResponse(TaskBase):
    id: int
    created_at: str
    updated_at: str
    assigned_users: Optional[List[int]] = None

    class Config:
        orm_mode = True
        from_attributes = True

    @validator('created_at', 'updated_at', pre=True)
    def datetime_to_str(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v

class TaskDetailResponse(TaskResponse):
    """Detailed task response including assignments and related entities"""
    assigned_users_details: Optional[List[UserBasicInfo]] = None
    comments: Optional[List[CommentResponse]] = None
    attachments: Optional[List[FileAttachmentResponse]] = None
    project: Optional[ProjectBasicInfo] = None

class TaskListResponse(BaseModel):
    """Response model for paginated task lists"""
    items: List[TaskResponse]
    total: int
    page: int
    page_size: int
    
class TaskFilterParams(BaseModel):
    """Parameters for filtering tasks in search operations"""
    status: Optional[List[StatusEnum]] = None
    priority: Optional[List[PriorityEnum]] = None
    due_date_from: Optional[date] = None
    due_date_to: Optional[date] = None
    assigned_to_user_id: Optional[int] = None
    project_id: Optional[int] = None
    search_term: Optional[str] = None

class TaskStatistics(BaseModel):
    """Task statistics response model"""
    total_tasks: int
    completed_tasks: int
    overdue_tasks: int
    tasks_by_status: Dict[str, int]
    tasks_by_priority: Dict[str, int]