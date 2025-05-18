import unittest
from unittest.mock import MagicMock, patch
from app.controllers.role_controller import RoleController
from app.models.dtos import RoleCreate, RoleUpdate, RoleResponse

class TestRoleController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.role_controller = RoleController(self.mock_db_session)

    @patch('app.repositories.role_repository.RoleRepository.create_role')
    def test_create_role(self, mock_create_role):
        role_data = RoleCreate(name="Test Role")
        mock_role = MagicMock()
        mock_role.id = 1
        mock_role.name = "Test Role"
        mock_create_role.return_value = mock_role

        response = self.role_controller.create_role(role_data)

        self.assertEqual(response.name, "Test Role")
        mock_create_role.assert_called_once_with(name="Test Role")

    @patch('app.repositories.role_repository.RoleRepository.get_role_by_id')
    def test_get_role(self, mock_get_role_by_id):
        mock_role = MagicMock()
        mock_role.id = 1
        mock_role.name = "Test Role"
        mock_get_role_by_id.return_value = mock_role

        response = self.role_controller.get_role(1)

        self.assertEqual(response.name, "Test Role")
        mock_get_role_by_id.assert_called_once_with(1)

    @patch('app.repositories.role_repository.RoleRepository.update_role')
    def test_update_role(self, mock_update_role):
        role_update = RoleUpdate(name="Updated Role")
        mock_role = MagicMock()
        mock_role.id = 1
        mock_role.name = "Updated Role"
        mock_update_role.return_value = mock_role

        response = self.role_controller.update_role(1, role_update)

        self.assertEqual(response.name, "Updated Role")
        mock_update_role.assert_called_once_with(1, name="Updated Role")

    @patch('app.repositories.role_repository.RoleRepository.delete_role')
    def test_delete_role(self, mock_delete_role):
        mock_delete_role.return_value = True

        response = self.role_controller.delete_role(1)

        self.assertEqual(response["message"], "Role deleted successfully")
        mock_delete_role.assert_called_once_with(1)

    @patch('app.repositories.role_repository.RoleRepository.list_roles')
    def test_get_all_roles(self, mock_list_roles):
        mock_role1 = MagicMock()
        mock_role1.id = 1
        mock_role1.name = "Role 1"

        mock_role2 = MagicMock()
        mock_role2.id = 2
        mock_role2.name = "Role 2"

        mock_list_roles.return_value = [mock_role1, mock_role2]

        response = self.role_controller.get_all_roles()

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].name, "Role 1")
        mock_list_roles.assert_called_once()

if __name__ == "__main__":
    unittest.main()