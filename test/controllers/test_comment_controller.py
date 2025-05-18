import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from app.controllers.comment_controller import CommentController
from app.models.dtos.task_dtos import CommentCreate, CommentUpdate


class TestCommentController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.comment_controller = CommentController(self.mock_db_session)
        self.created_at_str = datetime.utcnow().isoformat()

    @patch('app.repositories.comment_repository.CommentRepository.create_comment')
    @patch('app.repositories.comment_repository.CommentRepository.get_comment_by_id')
    def test_create_comment(self, mock_get_comment_by_id, mock_create_comment):
        comment_data = CommentCreate(task_id=1, user_id=1, content="Test comment")
        mock_comment = MagicMock(id=1, **comment_data.dict())
        mock_comment.created_at = self.created_at_str
        mock_user = MagicMock(id=1, first_name="Test", last_name="User", email="test@example.com")
        mock_create_comment.return_value = mock_comment
        mock_get_comment_by_id.return_value = (mock_comment, mock_user)

        response = self.comment_controller.create_comment(comment_data)

        self.assertEqual(response.content, "Test comment")
        self.assertEqual(response.user_id, 1)
        mock_create_comment.assert_called_once_with(comment_data)
        mock_get_comment_by_id.assert_called_once_with(1)

    @patch('app.repositories.comment_repository.CommentRepository.get_comment_by_id')
    def test_get_comment(self, mock_get_comment_by_id):
        mock_comment = MagicMock(id=1, content="Test comment", user_id=1)
        mock_comment.created_at = self.created_at_str
        mock_user = MagicMock(id=1, first_name="Test", last_name="User", email="test@example.com")
        mock_get_comment_by_id.return_value = (mock_comment, mock_user)

        response = self.comment_controller.get_comment(1)

        self.assertEqual(response.content, "Test comment")
        self.assertEqual(response.user_id, 1)
        mock_get_comment_by_id.assert_called_once_with(1)

    @patch('app.repositories.comment_repository.CommentRepository.get_comments_by_task')
    def test_get_task_comments(self, mock_get_comments_by_task):
        mock_comment = MagicMock(id=1, content="Test comment", user_id=1)
        mock_comment.created_at = self.created_at_str
        mock_user = MagicMock(id=1, first_name="Test", last_name="User", email="test@example.com")
        mock_get_comments_by_task.return_value = ([(mock_comment, mock_user)], 1)

        response = self.comment_controller.get_task_comments(task_id=1, page=1, page_size=10)

        self.assertEqual(len(response.items), 1)
        self.assertEqual(response.items[0].content, "Test comment")
        mock_get_comments_by_task.assert_called_once_with(task_id=1, page=1, page_size=10)

    @patch('app.repositories.comment_repository.CommentRepository.get_comment_by_id')
    @patch('app.repositories.comment_repository.CommentRepository.update_comment')
    def test_update_comment(self, mock_update_comment, mock_get_comment_by_id):
        mock_comment = MagicMock(id=1, content="Updated comment", user_id=1)
        mock_comment.created_at = self.created_at_str
        mock_user = MagicMock(id=1, first_name="Test", last_name="User", email="test@example.com")
        mock_get_comment_by_id.return_value = (mock_comment, mock_user)
        mock_update_comment.return_value = mock_comment

        comment_update = CommentUpdate(content="Updated comment")
        response = self.comment_controller.update_comment(1, comment_update, current_user_id=1)

        self.assertEqual(response.content, "Updated comment")
        mock_update_comment.assert_called_once_with(1, comment_update)
        mock_get_comment_by_id.assert_called_with(1)

    @patch('app.repositories.comment_repository.CommentRepository.get_comment_by_id')
    @patch('app.repositories.comment_repository.CommentRepository.delete_comment')
    def test_delete_comment(self, mock_delete_comment, mock_get_comment_by_id):
        mock_comment = MagicMock(id=1, content="Test comment", user_id=1)
        mock_comment.created_at = self.created_at_str
        mock_get_comment_by_id.return_value = (mock_comment, None)
        mock_delete_comment.return_value = True

        response = self.comment_controller.delete_comment(1, current_user_id=1)

        self.assertTrue(response)
        mock_delete_comment.assert_called_once_with(1)
