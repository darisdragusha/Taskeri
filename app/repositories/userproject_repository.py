from sqlalchemy.orm import Session
from models.userproject import UserProject
from models.user import User

class UserProjectRepository:
    """Handles operations related to project-user assignments."""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_user_to_project(self, user_id: int, project_id: int) -> UserProject:
        """Assign a user to a project."""
        assignment = UserProject(user_id=user_id, project_id=project_id)
        self.db_session.add(assignment)
        self.db_session.commit()
        return assignment

    def remove_user_from_project(self, user_id: int, project_id: int) -> bool:
        """Remove a user from a project."""
        deleted = self.db_session.query(UserProject).filter_by(
            user_id=user_id,
            project_id=project_id
        ).delete()
        self.db_session.commit()
        return deleted > 0

    def get_users_for_project(self, project_id: int) -> list[User]:
        """Get full user details for users assigned to a specific project."""
        return (
            self.db_session.query(User)
            .join(UserProject, User.id == UserProject.user_id)
            .filter(UserProject.project_id == project_id)
            .all()
        )