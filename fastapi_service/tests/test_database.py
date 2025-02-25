import unittest
from unittest.mock import patch, MagicMock
from fastapi_service.modules.database.model.database import Database

class TestDatabase(unittest.TestCase):
    
    """
    Unit tests for the `Database` singleton class.

    This test suite ensures that:
    - The singleton pattern is correctly implemented.
    - The database connection pool is properly initialized.
    - Connections can be acquired and released correctly.
    - The connection pool can be closed properly.
    """
    
    def setUp (
        self,
    ) -> None:
        
        """
        Reset the singleton instance before each test to ensure a clean state.
        """
        
        Database.instance = None

    @patch("fastapi_service.modules.database.model.database.pool.SimpleConnectionPool")
    def test_singleton_instance (
        self, 
        mock_pool,
    ) -> None:
        
        """
        Test that `Database` follows the singleton pattern.

        This test ensures that multiple instantiations of `Database` return the same instance.
        """
        
        db1 = Database()
        db2 = Database()
        self.assertIs(db1, db2)  

    @patch("fastapi_service.modules.database.model.database.pool.SimpleConnectionPool")
    def test_connect_initialization (
        self, 
        mock_pool,
    ) -> None:
        
        """
        Test that the database connection pool is initialized correctly.

        This test verifies that:
        - The `connect` method initializes a connection pool with correct parameters.
        - The connection pool is created only once per instance.
        """
        
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
        
        """
        Test acquiring a connection from the pool.

        This test ensures that:
        - The `get_connection` method retrieves a connection from the pool.
        - The retrieved connection matches the mock object.
        """
        
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
        
        """
        Test releasing a connection back to the pool.

        This test verifies that:
        - The `release_connection` method correctly returns a connection to the pool.
        """
        
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
        
        """
        Test closing all connections in the pool.

        This test ensures that:
        - The `close_all` method correctly closes all connections in the pool.
        """
        
        db = Database()
        db.connect()
        db.close_all()
        mock_pool.return_value.closeall.assert_called_once()

if __name__ == "__main__":
    unittest.main()
