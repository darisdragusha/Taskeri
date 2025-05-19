from fastapi import APIRouter, Depends, Request
from app.controllers.team_controller import TeamController
from app.models.dtos.team_dtos import TeamCreate, TeamUpdate, TeamResponse, TeamStatistics
from app.models.dtos.user_dtos import UserResponse
from typing import List
from app.utils import get_db
from app.auth import auth_service

router = APIRouter(tags=["Teams"])

# -----------------------------
# READ
# -----------------------------

@router.get("/teams", response_model=List[TeamResponse])
async def get_all_teams(
    request: Request,
    controller: TeamController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
) -> List[TeamResponse]:
    """
    Endpoint to retrieve all teams.

    Business logic:
    - Useful for dashboards, HR, and organization charts
    """
    return controller.get_all_teams()


@router.get("/teams/statistics", response_model=TeamStatistics)
async def get_team_statistics(
    request: Request,
    controller: TeamController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
) -> TeamStatistics:
    """
    Endpoint to retrieve team count per department.

    Business logic:
    - Used for reporting and organizational analysis
    """
    return controller.get_team_statistics()


@router.get("/teams/{team_id}", response_model=TeamResponse)
async def get_team(
    team_id: int,
    request: Request,
    controller: TeamController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
) -> TeamResponse:
    """
    Endpoint to get a team by ID.

    Business logic:
    - Users with access can view team details
    - Typically used for team management or HR insights
    """
    return controller.get_team(team_id)

# -----------------------------
# CREATE
# -----------------------------

@router.post("/teams", response_model=TeamResponse)
async def create_team(
    team_create: TeamCreate,
    request: Request,
    controller: TeamController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
) -> TeamResponse:
    """
    Endpoint to create a new team.

    Business logic:
    - Only authorized users should be able to create new teams
    - Team names should be unique within their department
    """
    return controller.create_team(team_create)

# -----------------------------
# UPDATE
# -----------------------------

@router.put("/teams/{team_id}", response_model=TeamResponse)
async def update_team(
    team_id: int,
    team_update: TeamUpdate,
    request: Request,
    controller: TeamController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
) -> TeamResponse:
    """
    Endpoint to update a team.

    Business logic:
    - Team structure changes should be authorized
    - Prevent duplicate names within the same department
    """
    return controller.update_team(team_id, team_update)

# -----------------------------
# DELETE
# -----------------------------

@router.delete("/teams/{team_id}", response_model=dict)
async def delete_team(
    team_id: int,
    request: Request,
    controller: TeamController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
) -> dict:
    """
    Endpoint to delete a team.

    Business logic:
    - Deletion should be restricted to administrators
    - Prevent deletion if team is assigned to active projects
    """
    return controller.delete_team(team_id)

@router.get("/teams/{team_id}/members", response_model=List[UserResponse])
async def get_team_members(
    team_id: int,
    request: Request,
    controller: TeamController = Depends(),
    current_user: dict = Depends(auth_service.verify_user)
):
    """
    Get all users assigned to a specific team.
    """
    return controller.get_team_members(team_id)
