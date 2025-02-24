import unittest
from typing import Any, List, Tuple, Optional

from grpc_service.modules.database.controller.database_controller import DatabaseController
from psycopg2.extensions import connection

class FakeCursor:
    
    def __init__ (
        self, 
        result: Optional[List[Tuple[Any, ...]]] = None, 
        rowcount: int = 1,
    ):
        self.result = result or []
        self.rowcount = rowcount
        self.executed_query = None
        self.executed_params = None
        self.description = None

    def execute (
        self, 
        query, 
        params=None,
    ) -> None:
        
        self.executed_query = query
        self.executed_params = params
        
        if "RETURNING" in query.upper():
            self.description = ("dummy",)
            if not self.result:
                self.result = [(self.rowcount,)]
        else:
            self.description = None

    def fetchall (
        self,
    ) -> List[Tuple[Any, ...]]:
        
        return self.result

    def fetchone (
        self,
    ) -> Optional[Tuple[Any, ...]]:
        
        return self.result[0] if self.result else None

    def __enter__ (
        self,
    ) -> None:
        
        return self

    def __exit__ (
        self, 
        exc_type, 
        exc_val, 
        exc_tb,
    ) -> None:
        
        pass

class FakeConnection:
    
    def __init__ (
        self, 
        cursor_result: Optional[List[Tuple[Any, ...]]] = None, 
        rowcount: int = 1,
    ) -> None:
        
        self.cursor_result = cursor_result
        self.rowcount = rowcount
        self.committed = False
        self.rolled_back = False

    def cursor (
        self,
    ) -> FakeCursor:
        
        return FakeCursor (
            self.cursor_result, 
            self.rowcount,
        )

    def commit (
        self,
    ) -> None:
        
        self.committed = True

    def rollback (
        self,
    ) -> None:
        
        self.rolled_back = True

class FakeDatabase:
    
    """
    A fake database to simulate connection pooling.
    """
    
    def __init__ (
        self, 
        cursor_result: Optional[List[Tuple[Any, ...]]] = None, 
        rowcount: int = 1,
    ) -> None:
        
        self.cursor_result = cursor_result
        self.rowcount = rowcount
        self.released = False

    def get_connection (
        self,
    ) -> connection:
        
        return FakeConnection (
            self.cursor_result, 
            self.rowcount,
        )

    def release_connection (
        self, 
        conn: connection,
    ) -> None:
        
        self.released = True

# --- Unit Tests for DatabaseController ---

class TestDatabaseController(unittest.TestCase):
    
    def setUp (
        self,
    ) -> None:
        
        self.fake_db = FakeDatabase (
            cursor_result=[(1, "Test Book", "Test Author", "2021-01-01 00:00:00")], 
            rowcount=1,
        )
        self.controller = DatabaseController()
        self.controller.db = self.fake_db

    def test_execute_get_query_valid (
        self,
    ) -> None:

        query = """
            SELECT * 
            FROM base_book
        """
        
        result = self.controller.execute_get_query(query)
        
        self.assertEqual (
            result, 
            [(1, "Test Book", "Test Author", "2021-01-01 00:00:00")],
        )
        self.assertTrue(self.fake_db.released)

    def test_execute_get_query_invalid_query (
        self,
    ) -> None:
        
        query = """
            UPDATE base_book 
            SET book_name='Test'
        """
        
        with self.assertRaises(ValueError):
            self.controller.execute_get_query(query)

    def test_execute_insert_query_valid (
        self,
    ) -> None:
        
        query = """
            INSERT INTO base_book 
            (book_name, author, uploaded_at)
            VALUES (%s, %s, NOW())
            RETURNING id;
        """
        
        inserted_id = self.controller.execute_insert_query (
            query, 
            params=("New Book", "New Author"),
        )
        
        self.assertEqual(inserted_id, 1)
        self.assertTrue(self.fake_db.released)

    def test_execute_delete_query_valid (
        self,
    ) -> None:
        
        query = """
            DELETE FROM base_book 
            WHERE id = %s
        """

        self.fake_db.rowcount = 1
        
        rowcount = self.controller.execute_delete_query (
            query, 
            params=(1,),
        )
        
        self.assertEqual(rowcount, 1)
        self.assertTrue(self.fake_db.released)

    def test_execute_edit_query_valid (
        self,
    ) -> None:
        
        query = """
            UPDATE base_book 
            SET book_name = %s 
            WHERE id = %s
        """

        self.fake_db.rowcount = 1
        
        rowcount = self.controller.execute_edit_query (
            query, 
            params=("Updated Book", 1),
        )
        
        self.assertEqual(rowcount, 1)
        self.assertTrue(self.fake_db.released)

    def test_execute_insert_query_invalid_query (
        self,
    ) -> None:
        
        query = """
            SELECT * 
            FROM base_book
        """
        
        with self.assertRaises(ValueError):
            self.controller.execute_insert_query (
                query, 
                params=("Test", "Test"),
            )

    def test_execute_delete_query_invalid_query (
        self,
    ) -> None:
        
        query = """
            SELECT * 
            FROM base_book
        """
        
        with self.assertRaises(ValueError):
            self.controller.execute_delete_query (
                query, 
                params=(1,),
            )

    def test_execute_edit_query_invalid_query (
        self,
    ) -> None:
        
        query = """
            SELECT * 
            FROM base_book
        """
        
        with self.assertRaises(ValueError):
            self.controller.execute_edit_query (
                query, 
                params=("Test",),
            )

if __name__ == '__main__':
    unittest.main()
