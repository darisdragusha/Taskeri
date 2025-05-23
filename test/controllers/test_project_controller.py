import unittest
from unittest.mock import MagicMock, patch
from datetime import date
from app.controllers.project_controller import ProjectController
from app.models.dtos.project_dtos import ProjectCreate, ProjectUpdate, ProjectResponse, ProjectStatistics

class TestProjectController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.project_controller = ProjectController(self.mock_db_session)

    @patch.object(ProjectController, '_validate_user_ids_exist')
    @patch('app.repositories.project_repository.ProjectRepository.create_project')
    def test_create_project(self, mock_create_project, mock_validate_user_ids):
        mock_validate_user_ids.return_value = None
        project_data = ProjectCreate(
            name="Test Project",
            description="A test project",
            start_date=date(2025, 5, 18),
            end_date=date(2025, 6, 18),
            status="In Progress",
            assigned_user_ids=[1, 2]
        )
        mock_project = MagicMock()
        mock_project.id = 1
        mock_project.name = "Test Project"
        mock_project.description = "A test project"
        mock_project.start_date = date(2025, 5, 18)
        mock_project.end_date = date(2025, 6, 18)
        mock_project.status = "In Progress"
        mock_create_project.return_value = mock_project

        response = self.project_controller.create_project(project_data)

        self.assertEqual(response.name, "Test Project")
        self.assertEqual(response.status, "In Progress")
        mock_create_project.assert_called_once_with(
            name="Test Project",
            description="A test project",
            start_date=date(2025, 5, 18),
            end_date=date(2025, 6, 18),
            status="In Progress",
            assigned_user_ids=[1, 2]
        )

    @patch('app.repositories.project_repository.ProjectRepository.get_project_by_id')
    def test_get_project(self, mock_get_project_by_id):
        mock_project = MagicMock()
        mock_project.id = 1
        mock_project.name = "Test Project"
        mock_project.description = "A test project"
        mock_project.start_date = date(2025, 5, 18)
        mock_project.end_date = date(2025, 6, 18)
        mock_project.status = "In Progress"
        mock_get_project_by_id.return_value = mock_project

        response = self.project_controller.get_project(1)

        self.assertEqual(response.name, "Test Project")
        mock_get_project_by_id.assert_called_once_with(1)

    @patch('app.repositories.project_repository.ProjectRepository.get_all_projects')
    def test_get_all_projects(self, mock_get_all_projects):
        mock_project1 = MagicMock()
        mock_project1.id = 1
        mock_project1.name = "Project 1"
        mock_project1.description = "Description 1"
        mock_project1.start_date = date(2025, 5, 18)
        mock_project1.end_date = date(2025, 6, 18)
        mock_project1.status = "Not Started"

        mock_project2 = MagicMock()
        mock_project2.id = 2
        mock_project2.name = "Project 2"
        mock_project2.description = "Description 2"
        mock_project2.start_date = date(2025, 7, 1)
        mock_project2.end_date = date(2025, 8, 1)
        mock_project2.status = "In Progress"

        mock_get_all_projects.return_value = [mock_project1, mock_project2]

        response = self.project_controller.get_all_projects()

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].name, "Project 1")
        self.assertEqual(response[1].name, "Project 2")
        mock_get_all_projects.assert_called_once()

    @patch('app.repositories.project_repository.ProjectRepository.update_project')
    def test_update_project(self, mock_update_project):
        project_update = ProjectUpdate(name="Updated Project")
        mock_project = MagicMock()
        mock_project.id = 1
        mock_project.name = "Updated Project"
        mock_project.description = "Updated description"
        mock_project.start_date = date(2025, 5, 18)
        mock_project.end_date = date(2025, 6, 18)
        mock_project.status = "Completed"
        mock_update_project.return_value = mock_project

        response = self.project_controller.update_project(1, project_update)

        self.assertEqual(response.name, "Updated Project")
        mock_update_project.assert_called_once_with(1, {"name": "Updated Project"}, assigned_user_ids=None)

    @patch('app.repositories.project_repository.ProjectRepository.delete_project')
    def test_delete_project(self, mock_delete_project):
        mock_delete_project.return_value = True

        response = self.project_controller.delete_project(1)

        self.assertEqual(response["message"], "Project deleted successfully")
        mock_delete_project.assert_called_once_with(1)

    @patch('app.repositories.project_repository.ProjectRepository.get_project_statistics')
    def test_get_project_statistics(self, mock_get_project_statistics):
        mock_statistics = {
            "Not Started": 5,
            "In Progress": 10,
            "Completed": 3,
            "On Hold": 2
        }
        mock_get_project_statistics.return_value = mock_statistics

        response = self.project_controller.get_project_statistics()

        self.assertEqual(response.not_started_projects, 5)
        self.assertEqual(response.in_progress_projects, 10)
        self.assertEqual(response.completed_projects, 3)
        self.assertEqual(response.on_hold_projects, 2)
        self.assertEqual(response.total_projects, 20)
        mock_get_project_statistics.assert_called_once()

if __name__ == "__main__":
    unittest.main()
