import unittest
from unittest.mock import MagicMock, patch
from app.controllers.role_permission_controller import RolePermissionController
from app.models.dtos.role_permission_dto import RolePermissionCreate
from app.models.role_permission import RolePermission

class TestRolePermissionController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.role_permission_controller = RolePermissionController(self.mock_db_session)

    @patch('app.repositories.role_permission_repository.RolePermissionRepository.create')
    def test_create_mapping(self, mock_create):
        mapping_data = RolePermissionCreate(role_id=1, permission_id=2)
        mock_mapping = MagicMock()
        mock_mapping.role_id = 1
        mock_mapping.permission_id = 2
        mock_create.return_value = mock_mapping

        response = self.role_permission_controller.create_mapping(mapping_data)

        self.assertEqual(response.role_id, 1)
        self.assertEqual(response.permission_id, 2)
        mock_create.assert_called_once_with(mapping_data)

    @patch('app.repositories.role_permission_repository.RolePermissionRepository.get_all')
    def test_get_all_mappings(self, mock_get_all):
        mock_mapping1 = MagicMock()
        mock_mapping1.role_id = 1
        mock_mapping1.permission_id = 2

        mock_mapping2 = MagicMock()
        mock_mapping2.role_id = 3
        mock_mapping2.permission_id = 4

        mock_get_all.return_value = [mock_mapping1, mock_mapping2]

        response = self.role_permission_controller.get_all_mappings()

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].role_id, 1)
        mock_get_all.assert_called_once()

    @patch('app.repositories.role_permission_repository.RolePermissionRepository.delete')
    def test_delete_mapping(self, mock_delete):
        mock_delete.return_value = True

        response = self.role_permission_controller.delete_mapping(1, 2)

        self.assertTrue(response)
        mock_delete.assert_called_once_with(1, 2)

if __name__ == "__main__":
    unittest.main()