import unittest
from unittest.mock import patch, MagicMock
from app.utils.db_utils import get_global_db, get_tenant_session, switch_schema
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

class TestDBUtils(unittest.TestCase):

    @patch("app.utils.db_utils.GlobalSessionLocal")
    def test_get_global_db(self, mock_global_session):
        mock_session = MagicMock(spec=Session)
        mock_global_session.return_value = mock_session

        with get_global_db() as db:
            self.assertEqual(db, mock_session)
        mock_session.close.assert_called_once()

    @patch("app.utils.db_utils.create_engine")
    @patch("app.utils.db_utils.sessionmaker")
    def test_get_tenant_session(self, mock_sessionmaker, mock_create_engine):
        mock_engine = MagicMock()
        mock_create_engine.return_value = mock_engine
        mock_session = MagicMock(spec=Session)
        mock_sessionmaker.return_value = lambda: mock_session

        session = get_tenant_session("tenant_test")
        self.assertEqual(session, mock_session)
        mock_create_engine.assert_called_once()

    

if __name__ == "__main__":
    unittest.main()