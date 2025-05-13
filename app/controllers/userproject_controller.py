from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.dtos.user_dtos import UserResponse
from repositories.userproject_repository import UserProjectRepository
from utils import get_db

class UserProjectController:
    """Controller class for assigning/removing users from projects."""

    def __init__(self, db_session: Session = Depends(get_db)):
        self.repository = UserProjectRepository(db_session)

    def add_user(self, user_id: int, project_id: int):
        try:
            return self.repository.add_user_to_project(user_id, project_id)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def remove_user(self, user_id: int, project_id: int):
        try:
            success = self.repository.remove_user_from_project(user_id, project_id)
            if not success:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not assigned to project")
            return {"message": "User removed from project"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    def get_users(self, project_id: int) -> list[UserResponse]:
        try:
            users = self.repository.get_users_for_project(project_id)
            return [UserResponse.from_orm(user) for user in users]
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(e)}"
            )