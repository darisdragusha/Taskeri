from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from repositories.project_repository import ProjectRepository
from utils import get_db
from models.user import User
from models.dtos.project_dtos import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectStatistics
from typing import List, Dict, Optional


class ProjectController:
    """Controller class for handling project operations."""

    def __init__(self, db_session: Session = Depends(get_db)):
        """
        Initialize the ProjectController with a database session.

        Args:
            db_session (Session): SQLAlchemy session provided by FastAPI dependency injection.
        """
        self.repository = ProjectRepository(db_session)

    def create_project(self, project_create: ProjectCreate) -> ProjectResponse:
        """
        Create a new project.

        Args:
            project_create (ProjectCreate): Data required to create a project.

        Returns:
            ProjectResponse: Created project serialized as a response model.

        Raises:
            HTTPException: If a database error occurs.
        """
        try:
            if project_create.assigned_user_ids:
                self._validate_user_ids_exist(project_create.assigned_user_ids)
            project = self.repository.create_project(
                name=project_create.name,
                description=project_create.description,
                start_date=project_create.start_date,
                end_date=project_create.end_date,
                status=project_create.status or "Not Started",
                assigned_user_ids=project_create.assigned_user_ids
            )
            return ProjectResponse.from_orm(project)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")

    def get_project(self, project_id: int) -> ProjectResponse:
        """
        Retrieve a single project by its ID.

        Args:
            project_id (int): Unique identifier of the project.

        Returns:
            ProjectResponse: Project data if found.

        Raises:
            HTTPException: If the project is not found or a database error occurs.
        """
        try:
            project = self.repository.get_project_by_id(project_id)
            if not project:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
            return ProjectResponse.from_orm(project)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")

    def get_all_projects(self) -> List[ProjectResponse]:
        """
        Retrieve all projects in the system.

        Returns:
            List[ProjectResponse]: List of all projects.

        Raises:
            HTTPException: If a database error occurs.
        """
        try:
            projects = self.repository.get_all_projects()
            return [ProjectResponse.from_orm(project) for project in projects]
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")

    def update_project(self, project_id: int, project_update: ProjectUpdate) -> ProjectResponse:
        """
        Update an existing project's information.

        Args:
            project_id (int): ID of the project to update.
            project_update (ProjectUpdate): Fields to update.

        Returns:
            ProjectResponse: Updated project data.

        Raises:
            HTTPException: If the project is not found or a database error occurs.
        """
        try:
            update_data = project_update.dict(exclude_unset=True)
            assigned_user_ids = update_data.pop("assigned_user_ids", None)
            if assigned_user_ids is not None:
                self._validate_user_ids_exist(assigned_user_ids)
            project = self.repository.update_project(
                project_id,
                update_data,
                assigned_user_ids=assigned_user_ids
            )
            if not project:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
            return ProjectResponse.from_orm(project)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")

    def delete_project(self, project_id: int) -> Dict[str, str]:
        """
        Delete a project by its ID.

        Args:
            project_id (int): ID of the project to delete.

        Returns:
            Dict[str, str]: Success message if deletion is successful.

        Raises:
            HTTPException: If the project is not found or a database error occurs.
        """
        try:
            project = self.repository.delete_project(project_id)
            if not project:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
            return {"message": "Project deleted successfully"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")

    def get_project_statistics(self) -> ProjectStatistics:
        """
        Retrieve aggregated statistics about project statuses.

        Returns:
            ProjectStatistics: Count of projects grouped by status.

        Raises:
            HTTPException: If a database error occurs.
        """
        try:
            stats = self.repository.get_project_statistics()
            return ProjectStatistics.from_dict(stats)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")


    def _validate_user_ids_exist(self, user_ids: List[int]) -> None:
        existing_ids = {
            user.id for user in self.repository.db_session.query(User)
            .filter(User.id.in_(user_ids)).all()
        }
        missing_ids = set(user_ids) - existing_ids
        if missing_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The following user IDs do not exist: {sorted(missing_ids)}"
            )
