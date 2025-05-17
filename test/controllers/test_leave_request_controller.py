import unittest
from datetime import date
from unittest.mock import MagicMock, patch
from app.controllers.leave_request_controller import LeaveRequestController
from app.models.dtos.leave_request_dtos import LeaveRequestCreate, LeaveRequestResponse

class TestLeaveRequestController(unittest.TestCase):

    def setUp(self):
        self.mock_db_session = MagicMock()
        self.leave_request_controller = LeaveRequestController(self.mock_db_session)

    @patch('app.repositories.leave_request_repository.LeaveRequestRepository.create_leave_request')
    def test_create_leave_request(self, mock_create_leave_request):
        leave_request_data = LeaveRequestCreate(
            leave_type="Sick Leave",
            start_date=date(2025, 5, 18),
            end_date=date(2025, 5, 20)
        )
        mock_leave_request = MagicMock()
        mock_leave_request.id = 1
        mock_leave_request.leave_type = "Sick Leave"
        mock_leave_request.start_date = date(2025, 5, 18)
        mock_leave_request.end_date = date(2025, 5, 20)
        mock_leave_request.status = "Pending"
        mock_create_leave_request.return_value = mock_leave_request

        response = self.leave_request_controller.create_leave_request(leave_request_data, user_id=1)

        self.assertEqual(response.leave_type, "Sick Leave")
        self.assertEqual(response.status, "Pending")
        mock_create_leave_request.assert_called_once_with(
            user_id=1,
            leave_type="Sick Leave",
            start_date=date(2025, 5, 18),
            end_date=date(2025, 5, 20),
            status="Pending"
        )

    @patch('app.repositories.leave_request_repository.LeaveRequestRepository.get_leave_request_by_id')
    def test_get_leave_request(self, mock_get_leave_request_by_id):
        mock_leave_request = MagicMock()
        mock_leave_request.id = 1
        mock_leave_request.leave_type = "Sick Leave"
        mock_leave_request.start_date = "2025-05-18"
        mock_leave_request.end_date = "2025-05-20"
        mock_leave_request.status = "Pending"
        mock_get_leave_request_by_id.return_value = mock_leave_request

        response = self.leave_request_controller.get_leave_request(1)

        self.assertEqual(response.leave_type, "Sick Leave")
        mock_get_leave_request_by_id.assert_called_once_with(1)

    @patch('app.repositories.leave_request_repository.LeaveRequestRepository.get_leave_requests_by_user')
    def test_get_leave_requests_by_user(self, mock_get_leave_requests_by_user):
        mock_leave_request1 = MagicMock()
        mock_leave_request1.id = 1
        mock_leave_request1.leave_type = "Sick Leave"
        mock_leave_request1.start_date = "2025-05-18"
        mock_leave_request1.end_date = "2025-05-20"
        mock_leave_request1.status = "Pending"

        mock_leave_request2 = MagicMock()
        mock_leave_request2.id = 2
        mock_leave_request2.leave_type = "Vacation"
        mock_leave_request2.start_date = "2025-06-01"
        mock_leave_request2.end_date = "2025-06-05"
        mock_leave_request2.status = "Pending"

        mock_get_leave_requests_by_user.return_value = [mock_leave_request1, mock_leave_request2]

        response = self.leave_request_controller.get_leave_requests_by_user(1)

        self.assertEqual(len(response), 2)
        self.assertEqual(response[0].leave_type, "Sick Leave")
        mock_get_leave_requests_by_user.assert_called_once_with(1)

    @patch('app.repositories.leave_request_repository.LeaveRequestRepository.update_leave_status')
    def test_update_leave_status(self, mock_update_leave_status):
        mock_leave_request = MagicMock()
        mock_leave_request.id = 1
        mock_leave_request.leave_type = "Sick Leave"
        mock_leave_request.start_date = "2025-05-18"
        mock_leave_request.end_date = "2025-05-20"
        mock_leave_request.status = "Approved"
        mock_update_leave_status.return_value = mock_leave_request

        response = self.leave_request_controller.update_leave_status(1, "Approved")

        self.assertEqual(response.status, "Approved")
        mock_update_leave_status.assert_called_once_with(1, "Approved")

    @patch('app.repositories.leave_request_repository.LeaveRequestRepository.delete_leave_request')
    def test_delete_leave_request(self, mock_delete_leave_request):
        mock_delete_leave_request.return_value = True

        response = self.leave_request_controller.delete_leave_request(1)

        self.assertEqual(response["message"], "Leave request deleted successfully")
        mock_delete_leave_request.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()
