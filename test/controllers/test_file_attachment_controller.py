import unittest
from unittest.mock import MagicMock, patch
from app.controllers.file_attachment_controller import FileAttachmentController
from app.models.dtos.file_attachment_dtos import FileAttachmentCreate, FileAttachmentUpdate
from app.models.file_attachment import FileAttachment

class TestFileAttachmentController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.file_attachment_controller = FileAttachmentController(self.mock_db_session)

    @patch('app.repositories.file_attachment_repository.FileAttachmentRepository.create')
    def test_create_attachment(self, mock_create):
        attachment_data = FileAttachmentCreate(task_id=1, file_path="/path/to/file")
        mock_attachment = MagicMock()
        mock_attachment.id = 1
        mock_attachment.task_id = 1
        mock_attachment.file_path = "/path/to/file"
        mock_create.return_value = mock_attachment

        response = self.file_attachment_controller.create_attachment(attachment_data)

        self.assertEqual(response.task_id, 1)
        self.assertEqual(response.file_path, "/path/to/file")
        mock_create.assert_called_once_with(attachment_data)

    @patch('app.repositories.file_attachment_repository.FileAttachmentRepository.get_all')
    def test_get_all_attachments(self, mock_get_all):
        mock_attachment1 = MagicMock()
        mock_attachment1.id = 1
        mock_attachment1.task_id = 1
        mock_attachment1.file_path = "/path/to/file1"

        mock_attachment2 = MagicMock()
        mock_attachment2.id = 2
        mock_attachment2.task_id = 2
        mock_attachment2.file_path = "/path/to/file2"

        mock_get_all.return_value = [mock_attachment1, mock_attachment2]

        response = self.file_attachment_controller.get_all_attachments()

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].file_path, "/path/to/file1")
        mock_get_all.assert_called_once()

    @patch('app.repositories.file_attachment_repository.FileAttachmentRepository.get_by_id')
    def test_get_attachment_by_id(self, mock_get_by_id):
        mock_attachment = MagicMock()
        mock_attachment.id = 1
        mock_attachment.task_id = 1
        mock_attachment.file_path = "/path/to/file"
        mock_get_by_id.return_value = mock_attachment

        response = self.file_attachment_controller.get_attachment_by_id(1)

        self.assertEqual(response.file_path, "/path/to/file")
        mock_get_by_id.assert_called_once_with(1)

    @patch('app.repositories.file_attachment_repository.FileAttachmentRepository.get_by_task_id')
    def test_get_attachments_by_task(self, mock_get_by_task_id):
        mock_attachment1 = MagicMock()
        mock_attachment1.id = 1
        mock_attachment1.task_id = 1
        mock_attachment1.file_path = "/path/to/file1"

        mock_attachment2 = MagicMock()
        mock_attachment2.id = 2
        mock_attachment2.task_id = 1
        mock_attachment2.file_path = "/path/to/file2"

        mock_get_by_task_id.return_value = [mock_attachment1, mock_attachment2]

        response = self.file_attachment_controller.get_attachments_by_task(1)

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].file_path, "/path/to/file1")
        mock_get_by_task_id.assert_called_once_with(1)

    @patch('app.repositories.file_attachment_repository.FileAttachmentRepository.update')
    def test_update_attachment(self, mock_update):
        attachment_update = FileAttachmentUpdate(file_path="/new/path/to/file")
        mock_attachment = MagicMock()
        mock_attachment.id = 1
        mock_attachment.task_id = 1
        mock_attachment.file_path = "/new/path/to/file"
        mock_update.return_value = mock_attachment

        response = self.file_attachment_controller.update_attachment(1, attachment_update)

        self.assertEqual(response.file_path, "/new/path/to/file")
        mock_update.assert_called_once_with(1, attachment_update)

    @patch('app.repositories.file_attachment_repository.FileAttachmentRepository.delete')
    def test_delete_attachment(self, mock_delete):
        mock_delete.return_value = True

        response = self.file_attachment_controller.delete_attachment(1)

        self.assertTrue(response)
        mock_delete.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()