from typing import Any, List, Optional, Tuple
from psycopg2.extensions import connection
from grpc_service.modules.database.model.database import Database 

class DatabaseController:
    
    """
    Controller class for executing database queries.

    This class provides methods to execute SELECT, INSERT, DELETE, and UPDATE queries
    using a singleton Database instance for connection pooling. It ensures proper
    transaction management (commit/rollback) and resource cleanup.
    """

    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the DatabaseController.
        """
        
        self.db = Database()

    def execute_get_query (
        self, 
        query: str,
    ) -> List[Tuple[Any, ...]]:
        
        """
        Executes a SELECT query and returns the result as a list of rows.

        Args:
            query (str): The SELECT query to execute.

        Raises:
            ValueError: If the provided query does not start with 'SELECT'.

        Returns:
            List[Tuple[Any, ...]]: A list of tuples representing the rows returned by the query.
        """
        
        if not query.strip().lower().startswith("select"):
            raise ValueError("Provided query is not a SELECT query.")

        connection_obj: connection = self.db.get_connection()
        try:
            with connection_obj.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
            connection_obj.commit()
            return result
        except Exception as e:
            connection_obj.rollback()
            raise e
        finally:
            self.db.release_connection(connection_obj)

    def execute_insert_query (
        self, 
        query: str, 
        params: Optional[Tuple[Any, ...]] = None,
    ) -> int:
        
        """
        Executes an INSERT query and returns the ID of the inserted row if available.

        Args:
            query (str): The INSERT query to execute.
            params (Optional[Tuple[Any, ...]]): Query parameters for the INSERT query.

        Raises:
            ValueError: If the provided query does not start with 'INSERT'.

        Returns:
            int: The ID of the inserted row if available; otherwise, -1.
        """
        
        if not query.strip().lower().startswith("insert"):
            raise ValueError("Provided query is not an INSERT query.")

        connection_obj: connection = self.db.get_connection()
        try:
            with connection_obj.cursor() as cursor:
                cursor.execute(query, params)
                inserted_id = cursor.fetchone()[0] if cursor.description else -1
            connection_obj.commit()
            return inserted_id
        except Exception as e:
            connection_obj.rollback()
            raise e
        finally:
            self.db.release_connection(connection_obj)

    def execute_delete_query (
        self, 
        query: str, 
        params: Optional[Tuple[Any, ...]] = None,
    ) -> int:
        
        """
        Executes a DELETE query and returns the number of rows affected.

        Args:
            query (str): The DELETE query to execute.
            params (Optional[Tuple[Any, ...]]): Query parameters for the DELETE query.

        Raises:
            ValueError: If the provided query does not start with 'DELETE'.

        Returns:
            int: The number of rows deleted.
        """
        
        if not query.strip().lower().startswith("delete"):
            raise ValueError("Provided query is not a DELETE query.")

        connection_obj: connection = self.db.get_connection()
        try:
            with connection_obj.cursor() as cursor:
                cursor.execute(query, params)
                rowcount = cursor.rowcount
            connection_obj.commit()
            return rowcount
        except Exception as e:
            connection_obj.rollback()
            raise e
        finally:
            self.db.release_connection(connection_obj)

    def execute_edit_query(
        self, 
        query: str, 
        params: Optional[Tuple[Any, ...]] = None,
    ) -> int:
        
        """
        Executes an UPDATE query and returns the number of rows affected.

        Args:
            query (str): The UPDATE query to execute.
            params (Optional[Tuple[Any, ...]]): Query parameters for the UPDATE query.

        Raises:
            ValueError: If the provided query does not start with 'UPDATE'.

        Returns:
            int: The number of rows updated.
        """
        
        if not query.strip().lower().startswith("update"):
            raise ValueError("Provided query is not an UPDATE query.")

        connection_obj: connection = self.db.get_connection()
        try:
            with connection_obj.cursor() as cursor:
                cursor.execute(query, params)
                rowcount = cursor.rowcount
            connection_obj.commit()
            return rowcount
        except Exception as e:
            connection_obj.rollback()
            raise e
        finally:
            self.db.release_connection(connection_obj)
