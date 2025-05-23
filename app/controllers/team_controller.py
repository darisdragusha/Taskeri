from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.repositories.team_repository import TeamRepository
from app.repositories.user_repository import UserRepository
from app.utils import get_db
from app.models.dtos.team_dtos import TeamCreate, TeamUpdate, TeamResponse, TeamStatistics
from app.models.dtos.user_dtos import UserResponse
from typing import List, Dict


class TeamController:
    """Controller class for handling team operations."""

    def __init__(self, db_session: Session = Depends(get_db)):
        self.repository = TeamRepository(db_session)
        self.user_repository = UserRepository(db_session)

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
            return TeamResponse.model_validate(team, from_attributes=True)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")

    def get_team(self, team_id: int) -> TeamResponse:
        """Retrieve a single team by its ID."""
        try:
            team = self.repository.get_team_by_id(team_id)
            if not team:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
            return TeamResponse.model_validate(team, from_attributes=True)
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")

    def get_all_teams(self) -> List[TeamResponse]:
        """Retrieve all teams."""
        try:
            teams = self.repository.get_all_teams()
            return [TeamResponse.model_validate(team, from_attributes=True) for team in teams]
        except SQLAlchemyError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"Database error: {str(e)}")

    def update_team(self, team_id: int, team_update: TeamUpdate) -> TeamResponse:
        """Update an existing team's information."""
        try:
            update_data = team_update.model_dump(exclude_unset=True)
            team = self.repository.update_team(team_id, update_data)
            if not team:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found")
            return TeamResponse.model_validate(team, from_attributes=True)
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
        
    def get_team_members(self, team_id: int) -> List[UserResponse]:
        """
        Retrieve all members assigned to a specific team.

        Args:
            team_id (int): The ID of the team whose members are to be fetched.

        Returns:
            List[UserResponse]: A list of users belonging to the specified team,
                                formatted as response DTOs.
        """
        users = self.user_repository.get_users_by_team(team_id)
        return [UserResponse.model_validate(user) for user in users]
