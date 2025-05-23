import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timezone
from app.controllers.user_controller import UserController
from app.models.dtos.user_dtos import UserCreate, UserUpdate, UserResponse
from app.models.dtos.role_dtos import RoleResponse


class TestUserController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.user_controller = UserController(self.mock_db_session)

        
        self.mock_repo = MagicMock()
        self.user_controller.repository = self.mock_repo

    @patch("app.controllers.user_controller.get_global_db")
    @patch("app.controllers.user_controller.TenantUserRepository")
    @patch("app.controllers.user_controller.send_account_creation_email")
    @patch("app.controllers.user_controller.hash_password", return_value="hashed123")
    def test_create_user(
        self,
        mock_hash_password,
        mock_send_email,
        mock_tenant_repo_class,
        mock_get_global_db
    ):
        user_data = UserCreate(
            email="test@example.com",
            password="securepass",
            first_name="Test",
            last_name="User",
            department_id=None,
            team_id=None
        )

        mock_user = UserResponse(
            id=1,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            department_id=None,
            team_id=None,
            role_id=2,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )

        # Patch the repository methods
        self.user_controller.repository = MagicMock()
        self.user_controller.repository.create_user.return_value = mock_user
        self.user_controller.repository.get_user_roles.return_value = [
            RoleResponse(id=2, name="Employee")
        ]
        self.user_controller.repository.assign_role_to_user = MagicMock()
        self.user_controller.repository.get_role_by_name.return_value = RoleResponse(id=2, name="Employee")

        # Tenant repo
        mock_tenant_repo = MagicMock()
        mock_tenant_repo_class.return_value = mock_tenant_repo
        mock_get_global_db.return_value.__enter__.return_value = MagicMock()

        current_user = {"tenant_name": "test_tenant"}

        response = self.user_controller.create_user(
            user_data, current_user, default_role_id=None
        )

        self.assertEqual(response.email, user_data.email)
        self.assertEqual(response.first_name, user_data.first_name)
        self.assertEqual(response.role_id, 2)

        # Ensure all key calls happened
        self.user_controller.repository.create_user.assert_called_once()
        self.user_controller.repository.assign_role_to_user.assert_called_once_with(1, 2)
        mock_tenant_repo_class.assert_called_once()
        mock_send_email.assert_called_once()
    def test_get_user(self):
        mock_user = MagicMock(
            id=1,
            email="test@example.com",
            first_name="Test",
            last_name="User",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        self.mock_repo.get_user_by_id.return_value = mock_user

        response = self.user_controller.get_user(1)

        self.assertEqual(response.email, "test@example.com")
        self.assertEqual(response.first_name, "Test")
        self.mock_repo.get_user_by_id.assert_called_once_with(1)

    def test_update_user(self):
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
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        self.mock_repo.update_user.return_value = mock_user

        response = self.user_controller.update_user(1, user_update)

        self.assertEqual(response.first_name, "Updated")
        self.assertEqual(response.last_name, "User")
        self.mock_repo.update_user.assert_called_once_with(
            1,
            first_name=user_update.first_name,
            last_name=user_update.last_name,
            department_id=user_update.department_id,
            team_id=user_update.team_id
        )

    def test_delete_user(self):
        self.mock_repo.delete_user.return_value = True

        response = self.user_controller.delete_user(1)

        self.assertEqual(response["message"], "User deleted successfully")
        self.mock_repo.delete_user.assert_called_once_with(1)

    def test_assign_role_to_user(self):
        self.mock_repo.assign_role_to_user.return_value = True

        response = self.user_controller.assign_role_to_user(1, 2)

        self.assertEqual(response["message"], "Role assigned successfully")
        self.mock_repo.assign_role_to_user.assert_called_once_with(1, 2)

    def test_remove_role_from_user(self):
        self.mock_repo.remove_role_from_user.return_value = True

        response = self.user_controller.remove_role_from_user(1, 2)

        self.assertEqual(response["message"], "Role removed successfully")
        self.mock_repo.remove_role_from_user.assert_called_once_with(1, 2)

    def test_get_user_roles(self):
        role1 = RoleResponse(id=1, name="Admin")
        role2 = RoleResponse(id=2, name="User")
        self.mock_repo.get_user_roles.return_value = [role1, role2]

        response = self.user_controller.get_user_roles(1)

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].name, "Admin")
        self.mock_repo.get_user_roles.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()