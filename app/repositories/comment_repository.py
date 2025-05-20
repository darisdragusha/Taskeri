from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional, Dict, Any, Tuple
from app.models.comment import Comment
from app.models.user import User
from app.models.dtos.task_dtos import CommentCreate, CommentUpdate


class CommentRepository:
    """Repository class for handling comment-related database operations."""

    def __init__(self, db_session: Session):
        """
        Initialize the CommentRepository.

        Args:
            db_session (Session): SQLAlchemy database session.
        """
        self.db_session = db_session

    def create_comment(self, data: CommentCreate) -> Comment:
        """
        Create a new comment record in the database.

        Args:
            data (CommentCreate): Comment creation data containing task_id, user_id, and content.

        Returns:
            Comment: The newly created comment object.
            
        Raises:
            Exception: If database operation fails.
        """
        try:
            comment = Comment(
                task_id=data.task_id,
                user_id=data.user_id,
                content=data.content
            )
            self.db_session.add(comment)
            self.db_session.commit()
            self.db_session.refresh(comment)
            return comment
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_comment_by_id(self, comment_id: int) -> Tuple[Optional[Comment], Optional[User]]:
        """
        Get a comment by its ID along with user information.

        Args:
            comment_id (int): Comment ID to retrieve.

        Returns:
            Tuple[Optional[Comment], Optional[User]]: Tuple of (Comment, User) if found, (None, None) otherwise.
        """
        comment = self.db_session.query(Comment).filter(Comment.id == comment_id).first()
        if not comment:
            return None, None
            
        user = self.db_session.query(User).filter(User.id == comment.user_id).first()
        return comment, user

    def get_comments_by_task(self, task_id: int, page: int = 1, page_size: int = 20) -> Tuple[List[Tuple[Comment, User]], int]:
        """
        Get paginated comments for a specific task along with user information.

        Args:
            task_id (int): Task ID to retrieve comments for.
            page (int): Page number (starting from 1).
            page_size (int): Number of comments per page.

        Returns:
            Tuple[List[Tuple[Comment, User]], int]: Tuple containing list of (Comment, User) pairs and total count.
        """
        # Get total count first
        total_count = self.db_session.query(Comment).filter(
            Comment.task_id == task_id
        ).count()
        
        # If no comments found, return empty list and zero count
        if total_count == 0:
            return [], 0
            
        # Calculate offset
        offset = (page - 1) * page_size
        
        # Get paginated comments
        comments = self.db_session.query(Comment).filter(
            Comment.task_id == task_id
        ).order_by(desc(Comment.created_at)).offset(offset).limit(page_size).all()
        
        # If no comments on this page, return empty list
        if not comments:
            return [], total_count
            
        # Get all user IDs from comments to fetch users in a single query (avoid N+1 query problem)
        user_ids = [comment.user_id for comment in comments]
        users = self.db_session.query(User).filter(User.id.in_(user_ids)).all()
        
        # Create a lookup dictionary for users by ID for efficient access
        user_dict = {user.id: user for user in users}
        
        # Pair each comment with its user
        return [(comment, user_dict.get(comment.user_id)) for comment in comments], total_count

    def update_comment(self, comment_id: int, data: CommentUpdate) -> Optional[Comment]:
        """
        Update an existing comment.

        Args:
            comment_id (int): ID of the comment to update.
            data (CommentUpdate): Comment data to update.

        Returns:
            Optional[Comment]: Updated comment if found, otherwise None.
            
        Raises:
            Exception: If database operation fails.
        """
        try:
            comment, _ = self.get_comment_by_id(comment_id)
            if not comment:
                return None

            comment.content = data.content
            self.db_session.commit()
            self.db_session.refresh(comment)
            return comment
        except Exception as e:
            self.db_session.rollback()
            raise e

    def delete_comment(self, comment_id: int) -> bool:
        """
        Delete a comment by ID.

        Args:
            comment_id (int): ID of the comment to delete.

        Returns:
            bool: True if comment was deleted, False if comment was not found.
            
        Raises:
            Exception: If database operation fails.
        """
        try:
            comment, _ = self.get_comment_by_id(comment_id)
            if not comment:
                return False

            self.db_session.delete(comment)
            self.db_session.commit()
            return True
        except Exception as e:
            self.db_session.rollback()
            raise e