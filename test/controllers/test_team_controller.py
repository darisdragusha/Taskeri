import unittest
from unittest.mock import MagicMock, patch
from app.controllers.team_controller import TeamController
from app.models.dtos.team_dtos import TeamCreate, TeamUpdate, TeamResponse, TeamStatistics
from datetime import date

class TestTeamController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.team_controller = TeamController(self.mock_db_session)

    @patch('app.repositories.team_repository.TeamRepository.create_team')
    def test_create_team(self, mock_create_team):
        team_data = TeamCreate(name="Test Team", department_id=1)
        mock_team = MagicMock()
        mock_team.id = 1
        mock_team.name = "Test Team"
        mock_team.department_id = 1
        mock_create_team.return_value = mock_team

        response = self.team_controller.create_team(team_data)

        self.assertEqual(response.name, "Test Team")
        self.assertEqual(response.department_id, 1)
        mock_create_team.assert_called_once_with(name="Test Team", department_id=1)

    @patch('app.repositories.team_repository.TeamRepository.get_team_by_id')
    def test_get_team(self, mock_get_team_by_id):
        mock_team = MagicMock()
        mock_team.id = 1
        mock_team.name = "Test Team"
        mock_team.department_id = 1
        mock_get_team_by_id.return_value = mock_team

        response = self.team_controller.get_team(1)

        self.assertEqual(response.name, "Test Team")
        mock_get_team_by_id.assert_called_once_with(1)

    @patch('app.repositories.team_repository.TeamRepository.get_all_teams')
    def test_get_all_teams(self, mock_get_all_teams):
        mock_team1 = MagicMock()
        mock_team1.id = 1
        mock_team1.name = "Team 1"
        mock_team1.department_id = 1

        mock_team2 = MagicMock()
        mock_team2.id = 2
        mock_team2.name = "Team 2"
        mock_team2.department_id = 2

        mock_get_all_teams.return_value = [mock_team1, mock_team2]

        response = self.team_controller.get_all_teams()

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].name, "Team 1")
        mock_get_all_teams.assert_called_once()

    @patch('app.repositories.team_repository.TeamRepository.update_team')
    def test_update_team(self, mock_update_team):
        team_update = TeamUpdate(name="Updated Team")
        mock_team = MagicMock()
        mock_team.id = 1
        mock_team.name = "Updated Team"
        mock_team.department_id = 1
        mock_update_team.return_value = mock_team

        response = self.team_controller.update_team(1, team_update)

        self.assertEqual(response.name, "Updated Team")
        mock_update_team.assert_called_once_with(1, {"name": "Updated Team"})

    @patch('app.repositories.team_repository.TeamRepository.delete_team')
    def test_delete_team(self, mock_delete_team):
        mock_delete_team.return_value = True

        response = self.team_controller.delete_team(1)

        self.assertEqual(response["message"], "Team deleted successfully")
        mock_delete_team.assert_called_once_with(1)

    @patch('app.repositories.team_repository.TeamRepository.count_teams_by_department')
    def test_get_team_statistics(self, mock_count_teams_by_department):
        mock_statistics = {
            1: 3,  # Department ID 1
            2: 5   # Department ID 2
        }
        mock_count_teams_by_department.return_value = mock_statistics

        response = self.team_controller.get_team_statistics()

        self.assertEqual(response.stats[1], 3)
        self.assertEqual(response.stats[2], 5)
        mock_count_teams_by_department.assert_called_once()

if __name__ == "__main__":
    unittest.main()