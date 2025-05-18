from typing import List, Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, Depends, status

from app.models.dtos.task_dtos import CommentCreate, CommentUpdate, CommentResponse, UserBasicInfo, CommentListResponse
from app.repositories.comment_repository import CommentRepository
from app.models.tenant.tasks.comment import Comment
from app.models.user import User
from app.utils.db_utils import get_db


class CommentController:
    """Controller class for handling comment-related operations."""

    def __init__(self, db_session: Session = Depends(get_db)):
        """
        Initialize the CommentController.

        Args:
            db_session (Session): SQLAlchemy database session.
        """
        self.repository = CommentRepository(db_session)

    def create_comment(self, data: CommentCreate) -> CommentResponse:
        """
        Create a new comment.

        Args:
            data (CommentCreate): Comment creation data.

        Returns:
            CommentResponse: The newly created comment.
            
        Raises:
            HTTPException: If there's a database error.
        """
        try:
            comment = self.repository.create_comment(data)
            # Fetch the created comment with user information
            comment_with_user = self.repository.get_comment_by_id(comment.id)
            return self._map_to_response(*comment_with_user)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred"
            )

    def get_comment(self, comment_id: int) -> Optional[CommentResponse]:
        """
        Get a comment by its ID.

        Args:
            comment_id (int): Comment ID.

        Returns:
            Optional[CommentResponse]: Comment if found, otherwise None.
            
        Raises:
            HTTPException: If there's a database error.
        """
        try:
            comment, user = self.repository.get_comment_by_id(comment_id)
            if not comment:
                return None
            return self._map_to_response(comment, user)
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred"
            )

    def get_task_comments(self, task_id: int, page: int = 1, page_size: int = 20) -> CommentListResponse:
        """
        Get paginated comments for a task.

        Args:
            task_id (int): Task ID.
            page (int): Page number (starting from 1).
            page_size (int): Number of comments per page.

        Returns:
            CommentListResponse: Paginated list of comments for the task.
            
        Raises:
            HTTPException: If there's a database error.
        """
        try:
            comments_with_users, total = self.repository.get_comments_by_task(
                task_id=task_id,
                page=page,
                page_size=page_size
            )
            
            comments = [self._map_to_response(comment, user) for comment, user in comments_with_users]
            
            return CommentListResponse(
                items=comments,
                total=total,
                page=page,
                page_size=page_size
            )
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred"
            )

    def update_comment(self, comment_id: int, data: CommentUpdate, current_user_id: int) -> CommentResponse:
        """
        Update a comment.

        Args:
            comment_id (int): Comment ID.
            data (CommentUpdate): Comment update data.
            current_user_id (int): ID of the user making the request.

        Returns:
            CommentResponse: Updated comment.

        Raises:
            HTTPException: If comment not found, user not authorized, or database error.
        """
        try:
            # Check if comment exists
            comment, _ = self.repository.get_comment_by_id(comment_id)
            if not comment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Comment with ID {comment_id} not found"
                )

            # Check if the current user is the comment author
            if comment.user_id != current_user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only edit your own comments"
                )

            # Update the comment
            updated_comment = self.repository.update_comment(comment_id, data)
            # Fetch the updated comment with user information
            comment_with_user = self.repository.get_comment_by_id(comment_id)
            return self._map_to_response(*comment_with_user)
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred"
            )

    def delete_comment(self, comment_id: int, current_user_id: int) -> bool:
        """
        Delete a comment.

        Args:
            comment_id (int): Comment ID.
            current_user_id (int): ID of the user making the request.

        Returns:
            bool: True if comment was deleted.

        Raises:
            HTTPException: If comment not found, user not authorized, or database error.
        """
        try:
            # Check if comment exists
            comment, _ = self.repository.get_comment_by_id(comment_id)
            if not comment:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Comment with ID {comment_id} not found"
                )

            # Check if the current user is the comment author
            if comment.user_id != current_user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only delete your own comments"
                )

            # Delete the comment
            success = self.repository.delete_comment(comment_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to delete comment"
                )
            return True
        except HTTPException:
            raise
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred"
            )
        
    def _map_to_response(self, comment: Comment, user: Optional[User] = None) -> CommentResponse:
        """
        Map a Comment model to a CommentResponse DTO with user information.
        
        Args:
            comment (Comment): Comment model to map.
            user (Optional[User]): User model associated with the comment.
            
        Returns:
            CommentResponse: Mapped response DTO with user information.
        """
        # Manually create the response to ensure datetime conversion
        response = CommentResponse(
            id=comment.id,
            content=comment.content,
            user_id=comment.user_id,
            task_id=comment.task_id,  
            created_at=comment.created_at  # This will trigger the validator
        )
        
        # Add user information if available
        if user:
            response.user = UserBasicInfo(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email
            )
            
        return response