from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.repositories.team_repository import TeamRepository
from app.utils import get_db
from app.models.dtos.team_dtos import TeamCreate, TeamUpdate, TeamResponse, TeamStatistics
from typing import List, Dict


class TeamController:
    """Controller class for handling team operations."""

    def __init__(self, db_session: Session = Depends(get_db)):
        self.repository = TeamRepository(db_session)

    def create_team(self, team_create: TeamCreate) -> TeamResponse:
        """
        Create a new team.

        Args:
            team_create (TeamCreate): Data required to create a team.

        Returns:
            TeamResponse: Created team serialized as a response model.
        """
        try:
            team = self.repository.create_team(
                name=team_create.name,
                department_id=team_create.department_id
            )
            return TeamResponse.from_orm(team)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")

    def get_team(self, team_id: int) -> TeamResponse:
        """Retrieve a single team by its ID."""
        try:
            team = self.repository.get_team_by_id(team_id)
            if not team:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
            return TeamResponse.from_orm(team)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")

    def get_all_teams(self) -> List[TeamResponse]:
        """Retrieve all teams."""
        try:
            teams = self.repository.get_all_teams()
            return [TeamResponse.from_orm(team) for team in teams]
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")

    def update_team(self, team_id: int, team_update: TeamUpdate) -> TeamResponse:
        """Update an existing team's information."""
        try:
            update_data = team_update.dict(exclude_unset=True)
            team = self.repository.update_team(team_id, update_data)
            if not team:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
            return TeamResponse.from_orm(team)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")

    def delete_team(self, team_id: int) -> Dict[str, str]:
        """Delete a team by its ID."""
        try:
            team = self.repository.delete_team(team_id)
            if not team:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
            return {"message": "Team deleted successfully"}
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")

    def get_team_statistics(self) -> TeamStatistics:
        """
        Count number of teams per department.

        Returns:
            TeamStatistics: Department-wise team counts.
        """
        try:
            stats = self.repository.count_teams_by_department()
            return TeamStatistics.from_dict(stats)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")
