import unittest
from unittest.mock import MagicMock, patch
from app.controllers.user_profile_controller import UserProfileController
from app.models.dtos.user_profile_dtos import UserProfileCreate, UserProfileUpdate
from app.models.user_profile import UserProfile

class TestUserProfileController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.user_profile_controller = UserProfileController(self.mock_db_session)

    @patch('app.repositories.user_profile_repository.UserProfileRepository.create')
    def test_create_profile(self, mock_create):
        profile_data = UserProfileCreate(
            user_id=1,
            bio="Test bio",
            profile_picture="test_picture.jpg"
        )
        mock_profile = MagicMock()
        mock_profile.user_id = 1
        mock_profile.bio = "Test bio"
        mock_profile.profile_picture = "test_picture.jpg"
        mock_create.return_value = mock_profile

        response = self.user_profile_controller.create_profile(profile_data)

        self.assertEqual(response.user_id, 1)
        self.assertEqual(response.bio, "Test bio")
        mock_create.assert_called_once_with(profile_data)

    @patch('app.repositories.user_profile_repository.UserProfileRepository.get_by_user_id')
    def test_get_profile_by_user_id(self, mock_get_by_user_id):
        mock_profile = MagicMock()
        mock_profile.user_id = 1
        mock_profile.bio = "Test bio"
        mock_profile.profile_picture = "test_picture.jpg"
        mock_get_by_user_id.return_value = mock_profile

        response = self.user_profile_controller.get_profile_by_user_id(1)

        self.assertEqual(response.user_id, 1)
        self.assertEqual(response.bio, "Test bio")
        mock_get_by_user_id.assert_called_once_with(1)

    @patch('app.repositories.user_profile_repository.UserProfileRepository.update')
    def test_update_profile(self, mock_update):
        profile_update = UserProfileUpdate(
            bio="Updated bio",
            profile_picture="updated_picture.jpg"
        )
        mock_profile = MagicMock()
        mock_profile.user_id = 1
        mock_profile.bio = "Updated bio"
        mock_profile.profile_picture = "updated_picture.jpg"
        mock_update.return_value = mock_profile

        response = self.user_profile_controller.update_profile(1, profile_update)

        self.assertEqual(response.user_id, 1)
        self.assertEqual(response.bio, "Updated bio")
        mock_update.assert_called_once_with(1, profile_update)

    @patch('app.repositories.user_profile_repository.UserProfileRepository.delete')
    def test_delete_profile(self, mock_delete):
        mock_delete.return_value = True

        response = self.user_profile_controller.delete_profile(1)

        self.assertTrue(response)
        mock_delete.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()