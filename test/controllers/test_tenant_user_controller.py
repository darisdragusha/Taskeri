import unittest
from unittest.mock import MagicMock, patch
from app.controllers.tenant_user_controller import TenantUserController
from app.models.dtos import TenantUserCreate, TenantUserOut
from fastapi import HTTPException

class TestTenantUserController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.tenant_user_controller = TenantUserController(self.mock_db_session)

    @patch('app.controllers.tenant_user_controller.create_new_tenant')
    @patch('app.utils.migration_runner.subprocess.run')
    @patch('app.repositories.TenantUserRepository.get_by_email')
    @patch('app.repositories.TenantUserRepository.create')
    def test_register_tenant_user_success(self, mock_create, mock_get_by_email, mock_subprocess_run, mock_create_new_tenant):
        user_data = TenantUserCreate(
            email="test@example.com",
            tenant_schema="test_schema",
            first_name="Test",
            last_name="User",
            password="password123"
        )
        mock_get_by_email.return_value = None
        mock_user = MagicMock()
        mock_user.email = "test@example.com"
        mock_user.tenant_schema = "test_schema"
        mock_create.return_value = mock_user
        mock_subprocess_run.return_value = MagicMock(returncode=0)  # Mock successful subprocess call

        response = self.tenant_user_controller.register_tenant_user(user_data)

        self.assertEqual(response.email, "test@example.com")
        mock_get_by_email.assert_called_once_with("test@example.com")
        mock_create_new_tenant.assert_called_once_with(self.mock_db_session, "test_schema")
        mock_create.assert_called_once_with(user_data)
        

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