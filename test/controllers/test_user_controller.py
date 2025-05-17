import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from app.controllers.user_controller import UserController
from app.models.dtos.user_dtos import UserCreate, UserUpdate, UserResponse
from collections import namedtuple


# Define this at the top of the test class or file
MockRole = namedtuple("MockRole", ["id", "name"])

class TestUserController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.user_controller = UserController(self.mock_db_session)

    @patch('app.repositories.UserRepository.create_user')
    def test_create_user(self, mock_create_user):
        user_data = UserCreate(
            email="test@example.com",
            password="password123",
            first_name="Test",
            last_name="User",
            department_id=None,
            team_id=None
        )
        mock_create_user.return_value = MagicMock(
            id=1,
            **user_data.dict(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        response = self.user_controller.create_user(user_data)

        self.assertEqual(response.email, user_data.email)
        self.assertEqual(response.first_name, user_data.first_name)
        mock_create_user.assert_called_once_with(
            email=user_data.email,
            password=user_data.password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            department_id=user_data.department_id,
            team_id=user_data.team_id
        )

    @patch('app.repositories.UserRepository.get_user_by_id')
    def test_get_user(self, mock_get_user_by_id):
        mock_user = MagicMock(
            id=1,
            email="test@example.com",
            first_name="Test",
            last_name="User",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        mock_get_user_by_id.return_value = mock_user

        response = self.user_controller.get_user(1)

        self.assertEqual(response.email, "test@example.com")
        self.assertEqual(response.first_name, "Test")
        mock_get_user_by_id.assert_called_once_with(1)

    @patch('app.repositories.UserRepository.update_user')
    def test_update_user(self, mock_update_user):
        user_update = UserUpdate(
            email="test@example.com",
            first_name="Updated",
            last_name="User",
            team_id="1"
        )
        mock_user = MagicMock(
            id=1,
            email="test@example.com",
            first_name="Updated",
            last_name="User",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        mock_update_user.return_value = mock_user

        response = self.user_controller.update_user(1, user_update)

        self.assertEqual(response.first_name, "Updated")
        self.assertEqual(response.last_name, "User")
        mock_update_user.assert_called_once_with(
            1,
            first_name=user_update.first_name,
            last_name=user_update.last_name,
            department_id=user_update.department_id,
            team_id=user_update.team_id
        )

    @patch('app.repositories.UserRepository.delete_user')
    def test_delete_user(self, mock_delete_user):
        mock_delete_user.return_value = True

        response = self.user_controller.delete_user(1)

        self.assertEqual(response["message"], "User deleted successfully")
        mock_delete_user.assert_called_once_with(1)

    @patch('app.repositories.UserRepository.assign_role_to_user')
    def test_assign_role_to_user(self, mock_assign_role_to_user):
        mock_assign_role_to_user.return_value = True

        response = self.user_controller.assign_role_to_user(1, 2)

        self.assertEqual(response["message"], "Role assigned successfully")
        mock_assign_role_to_user.assert_called_once_with(1, 2)

    @patch('app.repositories.UserRepository.remove_role_from_user')
    def test_remove_role_from_user(self, mock_remove_role_from_user):
        mock_remove_role_from_user.return_value = True

        response = self.user_controller.remove_role_from_user(1, 2)

        self.assertEqual(response["message"], "Role removed successfully")
        mock_remove_role_from_user.assert_called_once_with(1, 2)

    @patch('app.repositories.UserRepository.get_user_roles')
    def test_get_user_roles(self, mock_get_user_roles):
        mock_get_user_roles.return_value = [
            MockRole(id=1, name="Admin"),
            MockRole(id=2, name="User")
        ]

        response = self.user_controller.get_user_roles(1)

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0]["name"], "Admin")
        mock_get_user_roles.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()
