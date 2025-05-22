import unittest
from unittest.mock import patch, MagicMock
from app.utils.email_utils import send_account_creation_email

class TestEmailUtils(unittest.TestCase):

    @patch("app.utils.email_utils.FastMail.send_message")
    def test_send_account_creation_email(self, mock_send_message):
        mock_send_message.return_value = None

        send_account_creation_email("test@example.com", "Test", "password123")

        mock_send_message.assert_called_once()

if __name__ == "__main__":
    unittest.main()