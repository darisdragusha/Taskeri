import unittest
from unittest.mock import patch, MagicMock
from app.controllers.login_controller import LoginController
from app.utils import hash_password


class TestLoginController(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.mock_db = MagicMock()
        self.controller = LoginController(self.mock_db)

    @patch("app.controllers.login_controller.auth_service")
    @patch("app.controllers.login_controller.UserRepository")
    @patch("app.controllers.login_controller.TenantUserRepository")
    @patch("app.controllers.login_controller.get_env")
    async def test_authenticate_user_success(self, mock_get_env, mock_tenant_user_repo_cls, mock_user_repo_cls, mock_auth_service):
        mock_get_env.return_value = "taskeri_global"

        # TenantUserRepository mock
        mock_tenant_user = MagicMock()
        mock_tenant_user.tenant_schema = "mytenant"
        mock_tenant_user.id = 99
        mock_tenant_user_repo = MagicMock()
        mock_tenant_user_repo.get_by_email.return_value = mock_tenant_user
        mock_tenant_user_repo_cls.return_value = mock_tenant_user_repo

        # UserRepository mock
        mock_user = MagicMock()
        mock_user.id = 123
        mock_user.email = "user@example.com"
        mock_user.password_hash = hash_password("password123")
        mock_user_repo = MagicMock()
        mock_user_repo.get_user_by_email.return_value = mock_user
        mock_user_repo_cls.return_value = mock_user_repo

        # Token generation
        mock_auth_service.create_access_token.return_value = "mocked-token"

        result = await self.controller.authenticate_user("user@example.com", "password123")

        self.assertEqual(result, "mocked-token")
        mock_get_env.assert_called_once()
        mock_tenant_user_repo.get_by_email.assert_called_once_with("user@example.com")
        mock_user_repo.get_user_by_email.assert_called_once_with("user@example.com")
        mock_auth_service.create_access_token.assert_called_once_with(
            user_id=123, tenant_id=99, tenant_name="mytenant"
        )

    @patch("app.controllers.login_controller.auth_service")
    @patch("app.controllers.login_controller.UserRepository")
    @patch("app.controllers.login_controller.TenantUserRepository")
    @patch("app.controllers.login_controller.get_env")
    async def test_authenticate_user_invalid_password(self, mock_get_env, mock_tenant_user_repo_cls, mock_user_repo_cls, mock_auth_service):
        mock_get_env.return_value = "taskeri_global"

        mock_tenant_user = MagicMock()
        mock_tenant_user.tenant_schema = "testtenant"
        mock_tenant_user.id = 1
        mock_tenant_user_repo_cls.return_value.get_by_email.return_value = mock_tenant_user

        mock_user = MagicMock()
        mock_user.email = "test@example.com"
        mock_user.password_hash = hash_password("correct-password")
        mock_user_repo_cls.return_value.get_user_by_email.return_value = mock_user

        result = await self.controller.authenticate_user("test@example.com", "wrong-password")

        self.assertIsNone(result)
        mock_auth_service.create_access_token.assert_not_called()

    @patch("app.controllers.login_controller.TenantUserRepository")
    @patch("app.controllers.login_controller.get_env")
    async def test_authenticate_user_user_not_found(self, mock_get_env, mock_tenant_user_repo_cls):
        mock_get_env.return_value = "taskeri_global"
        mock_tenant_user_repo_cls.return_value.get_by_email.return_value = None

        result = await self.controller.authenticate_user("notfound@example.com", "somepassword")

        self.assertIsNone(result)
