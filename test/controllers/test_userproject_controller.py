import unittest
from unittest.mock import MagicMock, patch
from app.controllers.userproject_controller import UserProjectController
from app.models.dtos.user_dtos import UserResponse
from app.models.dtos.project_dtos import ProjectResponse

class TestUserProjectController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.user_project_controller = UserProjectController(self.mock_db_session)

    @patch('app.repositories.userproject_repository.UserProjectRepository.add_user_to_project')
    def test_add_user(self, mock_add_user_to_project):
        mock_add_user_to_project.return_value = {"message": "User added to project"}

        response = self.user_project_controller.add_user(1, 2)

        self.assertEqual(response["message"], "User added to project")
        mock_add_user_to_project.assert_called_once_with(1, 2)

    @patch('app.repositories.userproject_repository.UserProjectRepository.remove_user_from_project')
    def test_remove_user(self, mock_remove_user_from_project):
        mock_remove_user_from_project.return_value = True

        response = self.user_project_controller.remove_user(1, 2)

        self.assertEqual(response["message"], "User removed from project")
        mock_remove_user_from_project.assert_called_once_with(1, 2)

    @patch('app.repositories.userproject_repository.UserProjectRepository.get_users_for_project')
    def test_get_users(self, mock_get_users_for_project):
        mock_user1 = MagicMock()
        mock_user1.id = 1
        mock_user1.email = "user1@example.com"
        mock_user1.first_name = "User"
        mock_user1.last_name = "One"
        mock_user1.created_at = "2025-05-01T10:00:00"
        mock_user1.updated_at = "2025-05-10T10:00:00"

        mock_user2 = MagicMock()
        mock_user2.id = 2
        mock_user2.email = "user2@example.com"
        mock_user2.first_name = "User"
        mock_user2.last_name = "Two"
        mock_user2.created_at = "2025-05-02T10:00:00"
        mock_user2.updated_at = "2025-05-11T10:00:00"

        mock_get_users_for_project.return_value = [mock_user1, mock_user2]

        response = self.user_project_controller.get_users(1)

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].email, "user1@example.com")
        mock_get_users_for_project.assert_called_once_with(1)

    @patch('app.repositories.userproject_repository.UserProjectRepository.get_projects_for_user')
    def test_get_projects(self, mock_get_projects_for_user):
        mock_project1 = MagicMock()
        mock_project1.id = 1
        mock_project1.name = "Project 1"
        mock_project1.description = "Description 1"
        mock_project1.start_date = "2025-05-01"
        mock_project1.end_date = "2025-05-10"
        mock_project1.status = "In Progress"

        mock_project2 = MagicMock()
        mock_project2.id = 2
        mock_project2.name = "Project 2"
        mock_project2.description = "Description 2"
        mock_project2.start_date = "2025-05-02"
        mock_project2.end_date = "2025-05-11"
        mock_project2.status = "Not Started"

        mock_get_projects_for_user.return_value = [mock_project1, mock_project2]

        response = self.user_project_controller.get_projects(1)

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].name, "Project 1")
        mock_get_projects_for_user.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()