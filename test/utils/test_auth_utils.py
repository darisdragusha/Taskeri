import unittest
from app.utils.auth_utils import hash_password, verify_password

class TestAuthUtils(unittest.TestCase):

    def test_hash_password(self):
        password = "securepassword"
        hashed = hash_password(password)
        self.assertNotEqual(password, hashed)
        self.assertTrue(hashed.startswith("$argon2"))

    def test_verify_password(self):
        password = "securepassword"
        hashed = hash_password(password)
        self.assertTrue(verify_password(password, hashed))
        self.assertFalse(verify_password("wrongpassword", hashed))

if __name__ == "__main__":
    unittest.main()