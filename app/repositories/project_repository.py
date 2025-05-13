from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List, Tuple, Dict, Any
from models.project import Project
from models.userproject import UserProject
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
        status: str = "Not Started",
        assigned_user_ids: Optional[List[int]] = None
    ) -> Project:
        """
        Create a new project.

        Args:
            name (str): Project name.
            description (Optional[str]): Project description.
            start_date (date): Start date of the project.
            end_date (Optional[date]): End date of the project.
            status (str): Project status.
            assigned_user_ids (Optional[List[int]]): Users to assign to the project.

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
            self.db_session.flush()  # To get project.id before assigning users

            if assigned_user_ids:
                for user_id in assigned_user_ids:
                    self.db_session.add(UserProject(user_id=user_id, project_id=project.id))

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

    def update_project(
        self,
        project_id: int,
        update_data: Dict[str, Any],
        assigned_user_ids: Optional[List[int]] = None
    ) -> Optional[Project]:
        """
        Update an existing project and efficiently update user assignments.

        Args:
            project_id (int): ID of the project to update.
            update_data (Dict[str, Any]): Fields and their new values.
            assigned_user_ids (Optional[List[int]]): Updated user assignments.

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

            if assigned_user_ids is not None:
                current_assignments = self.db_session.query(UserProject).filter(
                    UserProject.project_id == project_id
                ).all()
                current_user_ids = {up.user_id for up in current_assignments}
                new_user_ids = set(assigned_user_ids)

                users_to_remove = current_user_ids - new_user_ids
                users_to_add = new_user_ids - current_user_ids

                if users_to_remove:
                    self.db_session.query(UserProject).filter(
                        UserProject.project_id == project_id,
                        UserProject.user_id.in_(users_to_remove)
                    ).delete(synchronize_session=False)

                for user_id in users_to_add:
                    self.db_session.add(UserProject(user_id=user_id, project_id=project_id))

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
                self.db_session.query(UserProject).filter(
                    UserProject.project_id == project_id
                ).delete()
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
