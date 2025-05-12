from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.orm import Session
from typing import List, Dict

from models.dtos.task_dtos import CommentCreate, CommentUpdate, CommentResponse, CommentListResponse
from controllers.comment_controller import CommentController
from utils.db_utils import get_db
from middleware.auth_middleware import get_current_user

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    data: CommentCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new comment for a task.
    
    The user_id will be automatically set to the current authenticated user.
    """
    # Set the user_id to the current authenticated user
    data.user_id = current_user.get("user_id")
    
    controller = CommentController(db)
    return controller.create_comment(data)


@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(
    comment_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get a specific comment by ID.
    
    Returns detailed comment information.
    """
    controller = CommentController(db)
    comment = controller.get_comment(comment_id)
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with ID {comment_id} not found"
        )
        
    return comment


@router.get("/task/{task_id}", response_model=CommentListResponse)
def get_task_comments(
    task_id: int,
    request: Request,
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    page_size: int = Query(20, ge=1, le=100, description="Number of comments per page"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get paginated comments for a specific task.
    
    Returns a paginated list of comments with user details, ordered by creation date (newest first).
    Use page and page_size parameters to navigate through comments for tasks with many comments.
    """
    controller = CommentController(db)
    return controller.get_task_comments(
        task_id=task_id, 
        page=page, 
        page_size=page_size
    )


@router.put("/{comment_id}", response_model=CommentResponse)
def update_comment(
    comment_id: int,
    data: CommentUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update a comment.
    
    Users can only update their own comments.
    """
    controller = CommentController(db)
    return controller.update_comment(
        comment_id=comment_id, 
        data=data, 
        current_user_id=current_user.get("user_id")
    )


@router.delete("/{comment_id}", response_model=Dict[str, str], status_code=status.HTTP_200_OK)
def delete_comment(
    comment_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a comment.
    
    Users can only delete their own comments.
    """
    controller = CommentController(db)
    controller.delete_comment(
        comment_id=comment_id, 
        current_user_id=current_user.get("user_id")
    )
    return {"message": "Comment deleted successfully"}