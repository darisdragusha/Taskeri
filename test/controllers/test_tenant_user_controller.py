import unittest
from unittest.mock import MagicMock, patch
from app.controllers.tenant_user_controller import TenantUserController
from app.models.dtos import TenantUserCreate, TenantUserOut
from fastapi import HTTPException

class TestTenantUserController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.tenant_user_controller = TenantUserController(self.mock_db_session)

    @patch('app.utils.tenant_setup.create_new_tenant', return_value=None)
    @patch('app.controllers.tenant_user_controller.get_tenant_session')
    @patch('app.repositories.PermissionRepository')
    @patch('app.repositories.RoleRepository')
    @patch('app.repositories.RolePermissionRepository')
    @patch('app.repositories.UserRepository')
    @patch('app.repositories.TenantUserRepository.get_by_email', return_value=None)
    @patch('app.repositories.TenantUserRepository.create')
    def test_register_tenant_user_success(
        self,
        mock_create,
        mock_get_by_email,
        mock_user_repo,
        mock_role_perm_repo,
        mock_role_repo,
        mock_perm_repo,
        mock_get_tenant_session,
        mock_create_new_tenant
    ):
        # Arrange
        user_data = TenantUserCreate(
            email="test@example.com",
            first_name="Test",
            last_name="User",
            password="password123",
            tenant_schema="testschema"
        )

        mock_user = MagicMock()
        mock_user.email = user_data.email
        mock_user.tenant_schema = user_data.tenant_schema
        mock_create.return_value = mock_user

        # Mock tenant DB session
        mock_tenant_db = MagicMock()
        mock_get_tenant_session.return_value = mock_tenant_db

        # Mock permission repo
        mock_perm_instance = MagicMock()
        mock_perm_instance.list_permissions.return_value = [
            MagicMock(name="read_company", id=1),
            MagicMock(name="create_company", id=2),
        ]
        mock_perm_repo.return_value = mock_perm_instance

        # Mock role repo
        mock_role_instance = MagicMock()
        mock_role_instance.list_roles.return_value = [
            MagicMock(name="Admin", id=10),
            MagicMock(name="Manager", id=11),
            MagicMock(name="Employee", id=12),
        ]
        mock_role_instance.get_role_by_name.return_value = MagicMock(id=10)
        mock_role_repo.return_value = mock_role_instance

        # Mock role-permission repo
        mock_role_perm_repo.return_value = MagicMock()

        # Mock user repo (inside tenant)
        mock_user_instance = MagicMock()
        mock_user_instance.get_user_by_email.return_value = MagicMock(id=999)
        mock_user_repo.return_value = mock_user_instance

        # Act
        result = self.controller.register_tenant_user(user_data)

        # Assert
        self.assertIsInstance(result, TenantUserOut)
        self.assertEqual(result.email, user_data.email)
        self.assertEqual(result.tenant_schema, user_data.tenant_schema)
        mock_create_new_tenant.assert_called_once_with(self.mock_db_session, user_data.tenant_schema)
        mock_create.assert_called_once_with(user_data)
        mock_get_tenant_session.assert_called_once()    
        
    @patch('app.repositories.TenantUserRepository.get_by_email')
    def test_register_tenant_user_email_exists(self, mock_get_by_email):
        user_data = TenantUserCreate(
            email="test@example.com",
            tenant_schema="test_schema",
            first_name="Test",
            last_name="User",
            password="password123"
        )
        mock_get_by_email.return_value = MagicMock()

        with self.assertRaises(HTTPException) as context:
            self.tenant_user_controller.register_tenant_user(user_data)

        self.assertEqual(context.exception.status_code, 400)
        self.assertEqual(context.exception.detail, "Email already exists.")
        mock_get_by_email.assert_called_once_with("test@example.com")

if __name__ == "__main__":
    unittest.main()