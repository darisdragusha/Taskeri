from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List, Tuple, Dict, Any
from models.project import Project
from datetime import date


class ProjectRepository:
    """Repository for managing project-related database operations."""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_project(
        self,
        name: str,
        description: Optional[str],
        start_date: date,
        end_date: Optional[date] = None,
        status: str = "Not Started"
    ) -> Project:
        """
        Create a new project.

        Args:
            name (str): Project name.
            description (Optional[str]): Project description.
            start_date (date): Start date of the project.
            end_date (Optional[date]): End date of the project.
            status (str): Project status.

        Returns:
            Project: Newly created project instance.
        """
        try:
            project = Project(
                name=name,
                description=description,
                start_date=start_date,
                end_date=end_date,
                status=status
            )
            self.db_session.add(project)
            self.db_session.commit()
            self.db_session.refresh(project)
            return project
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_project_by_id(self, project_id: int) -> Optional[Project]:
        """Retrieve a project by its ID."""
        return self.db_session.query(Project).filter(Project.id == project_id).first()

    def get_all_projects(self) -> List[Project]:
        """Retrieve all projects."""
        return self.db_session.query(Project).order_by(Project.created_at.desc()).all()

    def update_project(self, project_id: int, update_data: Dict[str, Any]) -> Optional[Project]:
        """
        Update an existing project.

        Args:
            project_id (int): ID of the project to update.
            update_data (Dict[str, Any]): Fields and their new values.

        Returns:
            Optional[Project]: Updated project or None if not found.
        """
        try:
            project = self.get_project_by_id(project_id)
            if not project:
                return None

            for key, value in update_data.items():
                if hasattr(project, key) and value is not None:
                    setattr(project, key, value)

            self.db_session.commit()
            self.db_session.refresh(project)
            return project
        except Exception as e:
            self.db_session.rollback()
            raise e

    def delete_project(self, project_id: int) -> Optional[Project]:
        """
        Delete a project by ID.

        Returns:
            Optional[Project]: The deleted project or None if not found.
        """
        try:
            project = self.get_project_by_id(project_id)
            if project:
                self.db_session.delete(project)
                self.db_session.commit()
                return project
            return None
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_project_statistics(self) -> Dict[str, int]:
        """
        Generate basic statistics for projects.

        Returns:
            Dict[str, int]: Dictionary containing status-wise counts.
        """
        statuses = ["Not Started", "In Progress", "Completed", "On Hold"]
        stats = {}
        for status in statuses:
            count = self.db_session.query(func.count(Project.id)).filter(Project.status == status).scalar()
            stats[status] = count
        return stats
