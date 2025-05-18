import unittest
from unittest.mock import MagicMock, patch
from app.controllers.attendance_controller import AttendanceController
from app.models.attendance import Attendance
from datetime import datetime

class TestAttendanceController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.attendance_controller = AttendanceController(self.mock_db_session)

    @patch('app.repositories.attendance_repository.AttendanceRepository.create_attendance')
    def test_create_attendance(self, mock_create_attendance):
        check_in_time = datetime(2025, 5, 17, 10, 0, 0)
        mock_attendance = MagicMock(id=1, user_id=1, check_in=check_in_time)
        mock_create_attendance.return_value = mock_attendance

        response = self.attendance_controller.create_attendance(user_id=1)

        self.assertEqual(response.user_id, 1)
        mock_create_attendance.assert_called_once()
        called_args = mock_create_attendance.call_args[1]
        self.assertEqual(called_args['user_id'], 1)
        self.assertIsInstance(called_args['check_in'], datetime)

    @patch('app.repositories.attendance_repository.AttendanceRepository.close_open_attendance')
    def test_close_attendance(self, mock_close_open_attendance):
        check_out_time = datetime(2025, 5, 17, 18, 0, 0)
        mock_attendance = MagicMock(id=1, user_id=1, check_out=check_out_time)
        mock_close_open_attendance.return_value = mock_attendance

        response = self.attendance_controller.close_attendance(user_id=1)

        self.assertEqual(response.user_id, 1)
        mock_close_open_attendance.assert_called_once()
        called_args = mock_close_open_attendance.call_args[1]
        self.assertEqual(called_args['user_id'], 1)
        self.assertIsInstance(called_args['check_out'], datetime)

    @patch('app.repositories.attendance_repository.AttendanceRepository.get_attendance_for_user')
    def test_get_user_attendance(self, mock_get_attendance_for_user):
        mock_attendance_list = [
            MagicMock(id=1, user_id=1, check_in=datetime(2025, 5, 17, 10, 0), check_out=datetime(2025, 5, 17, 18, 0)),
            MagicMock(id=2, user_id=1, check_in=datetime(2025, 5, 16, 10, 0), check_out=datetime(2025, 5, 16, 18, 0))
        ]
        mock_get_attendance_for_user.return_value = mock_attendance_list

        response = self.attendance_controller.get_user_attendance(user_id=1)

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].user_id, 1)
        mock_get_attendance_for_user.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()
