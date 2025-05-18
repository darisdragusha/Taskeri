import unittest
from unittest.mock import MagicMock, patch
from app.controllers.permission_controller import PermissionController
from app.models.dtos.permission_dtos import PermissionCreate, PermissionUpdate, PermissionResponse

class TestPermissionController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.permission_controller = PermissionController(self.mock_db_session)

    @patch('app.repositories.permission_repository.PermissionRepository.create_permission')
    def test_create_permission(self, mock_create_permission):
        permission_data = PermissionCreate(name="Test Permission")
        mock_permission = MagicMock()
        mock_permission.id = 1
        mock_permission.name = "Test Permission"
        mock_create_permission.return_value = mock_permission

        response = self.permission_controller.create_permission(permission_data)

        self.assertEqual(response.name, "Test Permission")
        mock_create_permission.assert_called_once_with(name="Test Permission")

    @patch('app.repositories.permission_repository.PermissionRepository.get_permission_by_id')
    def test_get_permission(self, mock_get_permission_by_id):
        mock_permission = MagicMock()
        mock_permission.id = 1
        mock_permission.name = "Test Permission"
        mock_get_permission_by_id.return_value = mock_permission

        response = self.permission_controller.get_permission(1)

        self.assertEqual(response.name, "Test Permission")
        mock_get_permission_by_id.assert_called_once_with(1)

    @patch('app.repositories.permission_repository.PermissionRepository.update_permission')
    def test_update_permission(self, mock_update_permission):
        permission_update = PermissionUpdate(name="Updated Permission")
        mock_permission = MagicMock()
        mock_permission.id = 1
        mock_permission.name = "Updated Permission"
        mock_update_permission.return_value = mock_permission

        response = self.permission_controller.update_permission(1, permission_update)

        self.assertEqual(response.name, "Updated Permission")
        mock_update_permission.assert_called_once_with(1, name="Updated Permission")

    @patch('app.repositories.permission_repository.PermissionRepository.delete_permission')
    def test_delete_permission(self, mock_delete_permission):
        mock_delete_permission.return_value = True

        response = self.permission_controller.delete_permission(1)

        self.assertEqual(response["message"], "Permission deleted successfully")
        mock_delete_permission.assert_called_once_with(1)

    @patch('app.repositories.permission_repository.PermissionRepository.list_permissions')
    def test_get_all_permissions(self, mock_list_permissions):
        mock_permission1 = MagicMock()
        mock_permission1.id = 1
        mock_permission1.name = "Permission 1"

        mock_permission2 = MagicMock()
        mock_permission2.id = 2
        mock_permission2.name = "Permission 2"

        mock_list_permissions.return_value = [mock_permission1, mock_permission2]

        response = self.permission_controller.get_all_permissions()

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].name, "Permission 1")
        mock_list_permissions.assert_called_once()

if __name__ == "__main__":
    unittest.main()