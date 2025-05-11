from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List, Dict, Any
from models.team import Team
from models.department import Department


class TeamRepository:
    """Repository for managing team-related database operations."""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_team(self, name: str, department_id: int) -> Team:
        """
        Create a new team.

        Args:
            name (str): Team name.
            department_id (int): ID of the department the team belongs to.

        Returns:
            Team: Newly created team instance.
        """
        try:
            team = Team(name=name, department_id=department_id)
            self.db_session.add(team)
            self.db_session.commit()
            self.db_session.refresh(team)
            return team
        except Exception as e:
            self.db_session.rollback()
            raise e

    def get_team_by_id(self, team_id: int) -> Optional[Team]:
        """Retrieve a team by its ID."""
        return self.db_session.query(Team).filter(Team.id == team_id).first()

    def get_all_teams(self) -> List[Team]:
        """Retrieve all teams."""
        return self.db_session.query(Team).order_by(Team.id).all()

    def update_team(self, team_id: int, update_data: Dict[str, Any]) -> Optional[Team]:
        """
        Update an existing team.

        Args:
            team_id (int): ID of the team to update.
            update_data (Dict[str, Any]): Fields and their new values.

        Returns:
            Optional[Team]: Updated team or None if not found.
        """
        try:
            team = self.get_team_by_id(team_id)
            if not team:
                return None

            for key, value in update_data.items():
                if hasattr(team, key) and value is not None:
                    setattr(team, key, value)

            self.db_session.commit()
            self.db_session.refresh(team)
            return team
        except Exception as e:
            self.db_session.rollback()
            raise e

    def delete_team(self, team_id: int) -> Optional[Team]:
        """
        Delete a team by ID.

        Returns:
            Optional[Team]: The deleted team or None if not found.
        """
        try:
            team = self.get_team_by_id(team_id)
            if team:
                self.db_session.delete(team)
                self.db_session.commit()
                return team
            return None
        except Exception as e:
            self.db_session.rollback()
            raise e

    def count_teams_by_department(self) -> Dict[int, int]:
        """
        Count how many teams belong to each department.

        Returns:
            Dict[int, int]: Mapping of department_id to number of teams.
        """
        results = (
            self.db_session.query(Team.department_id, func.count(Team.id))
            .group_by(Team.department_id)
            .all()
        )
        return {dept_id: count for dept_id, count in results}
