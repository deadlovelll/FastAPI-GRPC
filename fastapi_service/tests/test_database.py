import unittest
from unittest.mock import patch, MagicMock
from fastapi_service.modules.database.model.database import Database

class TestDatabase(unittest.TestCase):
    
    def setUp (
        self,
    ) -> None:
        
        Database.instance = None

    @patch("fastapi_service.modules.database.model.database.pool.SimpleConnectionPool")
    def test_singleton_instance (
        self, 
        mock_pool,
    ) -> None:
        
        db1 = Database()
        db2 = Database()
        self.assertIs(db1, db2)  

    @patch("fastapi_service.modules.database.model.database.pool.SimpleConnectionPool")
    def test_connect_initialization (
        self, 
        mock_pool,
    ) -> None:
        
        db = Database()
        db.connect()
        mock_pool.assert_called_once_with (
            1, 
            20, 
            host='localhost', 
            user='test_task', 
            password='Lovell32bd', 
            database='test_task_database',
        )

    @patch("fastapi_service.modules.database.model.database.pool.SimpleConnectionPool")
    def test_get_connection (
        self, 
        mock_pool,
    ) -> None:
        
        mock_conn = MagicMock()
        mock_pool.return_value.getconn.return_value = mock_conn
        
        db = Database()
        db.connect()
        conn = db.get_connection()
        
        self.assertEqual (
            conn, 
            mock_conn,
        )
        mock_pool.return_value.getconn.assert_called_once()

    @patch("fastapi_service.modules.database.model.database.pool.SimpleConnectionPool")
    def test_release_connection (
        self, 
        mock_pool,
    ) -> None:
        
        mock_conn = MagicMock()
        db = Database()
        db.connect()
        db.release_connection(mock_conn)
        mock_pool.return_value.putconn.assert_called_once_with(mock_conn)

    @patch("fastapi_service.modules.database.model.database.pool.SimpleConnectionPool")
    def test_close_all (
        self, 
        mock_pool,
    ) -> None:
        
        db = Database()
        db.connect()
        db.close_all()
        mock_pool.return_value.closeall.assert_called_once()

if __name__ == "__main__":
    unittest.main()
