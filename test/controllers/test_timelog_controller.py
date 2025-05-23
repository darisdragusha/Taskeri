import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from app.controllers.timelog_controller import TimeLogController
from app.models.dtos.timelog_dtos import TimeLogCreate, TimeLogUpdate, TimeLogResponse

class TestTimeLogController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.timelog_controller = TimeLogController(self.mock_db_session)

    # Corrected test_create_time_log to include user_id parameter
    @patch('app.repositories.timelog_repository.TimeLogRepository.create_time_log')
    def test_create_time_log(self, mock_create_time_log):
        time_log_data = TimeLogCreate(
            task_id=2,
            start_time=datetime(2025, 5, 18, 9, 0),
            end_time=datetime(2025, 5, 18, 10, 0)
        )
        mock_time_log = MagicMock()
        mock_time_log.id = 1
        mock_time_log.user_id = 1
        mock_time_log.task_id = 2
        mock_time_log.start_time = datetime(2025, 5, 18, 9, 0)
        mock_time_log.end_time = datetime(2025, 5, 18, 10, 0)
        mock_time_log.duration = 60
        mock_create_time_log.return_value = mock_time_log

        response = self.timelog_controller.create_time_log(1, time_log_data)

        self.assertEqual(response.id, 1)
        self.assertEqual(response.duration, 60)
        mock_create_time_log.assert_called_once_with(user_id=1, data=time_log_data)

    @patch('app.repositories.timelog_repository.TimeLogRepository.get_time_log_by_id')
    def test_get_time_log(self, mock_get_time_log_by_id):
        mock_time_log = MagicMock()
        mock_time_log.id = 1
        mock_time_log.user_id = 1
        mock_time_log.task_id = 2
        mock_time_log.start_time = datetime(2025, 5, 18, 9, 0)
        mock_time_log.end_time = datetime(2025, 5, 18, 10, 0)
        mock_time_log.duration = 60
        mock_get_time_log_by_id.return_value = mock_time_log

        response = self.timelog_controller.get_time_log(1)

        self.assertEqual(response.id, 1)
        self.assertEqual(response.duration, 60)
        mock_get_time_log_by_id.assert_called_once_with(1)

    @patch('app.repositories.timelog_repository.TimeLogRepository.get_time_logs_by_user')
    def test_get_time_logs_by_user(self, mock_get_time_logs_by_user):
        mock_time_log1 = MagicMock()
        mock_time_log1.id = 1
        mock_time_log1.user_id = 1
        mock_time_log1.task_id = 2

        mock_time_log2 = MagicMock()
        mock_time_log2.id = 2
        mock_time_log2.user_id = 1
        mock_time_log2.task_id = 3

        mock_get_time_logs_by_user.return_value = [mock_time_log1, mock_time_log2]

        response = self.timelog_controller.get_time_logs_by_user(1)

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].id, 1)
        mock_get_time_logs_by_user.assert_called_once_with(1)

    @patch('app.repositories.timelog_repository.TimeLogRepository.update_time_log')
    def test_update_time_log(self, mock_update_time_log):
        time_log_update = TimeLogUpdate(
            start_time=datetime(2025, 5, 18, 9, 30),
            end_time=datetime(2025, 5, 18, 10, 30)
        )
        mock_time_log = MagicMock()
        mock_time_log.id = 1
        mock_time_log.user_id = 1
        mock_time_log.task_id = 2
        mock_time_log.start_time = datetime(2025, 5, 18, 9, 30)
        mock_time_log.end_time = datetime(2025, 5, 18, 10, 30)
        mock_time_log.duration = 60
        mock_update_time_log.return_value = mock_time_log

        response = self.timelog_controller.update_time_log(1, time_log_update)

        self.assertEqual(response.id, 1)
        self.assertEqual(response.duration, 60)
        mock_update_time_log.assert_called_once_with(1, time_log_update)

    @patch('app.repositories.timelog_repository.TimeLogRepository.delete_time_log')
    def test_delete_time_log(self, mock_delete_time_log):
        mock_delete_time_log.return_value = True

        response = self.timelog_controller.delete_time_log(1)

        self.assertTrue(response)
        mock_delete_time_log.assert_called_once_with(1)

    @patch('app.repositories.timelog_repository.TimeLogRepository.get_user_logs_by_time_range')
    def test_get_user_logs_by_time_range(self, mock_get_user_logs_by_time_range):
        mock_time_log1 = MagicMock()
        mock_time_log1.id = 1
        mock_time_log1.user_id = 1
        mock_time_log1.task_id = 2

        mock_time_log2 = MagicMock()
        mock_time_log2.id = 2
        mock_time_log2.user_id = 1
        mock_time_log2.task_id = 3

        mock_get_user_logs_by_time_range.return_value = [mock_time_log1, mock_time_log2]

        start_time = datetime(2025, 5, 18, 0, 0)
        end_time = datetime(2025, 5, 18, 23, 59)
        response = self.timelog_controller.get_user_logs_by_time_range(1, start_time, end_time)

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].id, 1)
        mock_get_user_logs_by_time_range.assert_called_once_with(1, start_time, end_time)

if __name__ == "__main__":
    unittest.main()