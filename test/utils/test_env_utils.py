import unittest
from unittest.mock import patch
from app.utils.env_utils import get_env, EnvironmentVariable

class TestEnvUtils(unittest.TestCase):

    @patch("os.getenv")
    def test_get_env(self, mock_getenv):
        mock_getenv.return_value = "test_value"
        value = get_env(EnvironmentVariable.DB_HOST)
        self.assertEqual(value, "test_value")
        mock_getenv.assert_called_once_with("DB_HOST", None)



if __name__ == "__main__":
    unittest.main()