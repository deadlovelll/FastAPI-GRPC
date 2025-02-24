import os
import psycopg2
from psycopg2 import pool
from typing import Optional

class Database:
    
    instance: Optional['Database'] = None
    pool: Optional[psycopg2.pool.SimpleConnectionPool] = None

    def __new__ (
        cls,
    ) -> 'Database':
        
        """
        Ensures only a single instance of the Database class is created.

        Returns:
            Database: The singleton instance of the Database class.
        """
        
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.instance.pool = None
        return cls.instance
    
    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes database connection details from environment variables.
        """
        
        self.host = os.getenv('DB_HOST')
        self.db_user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_NAME')
    
    def connect (
        self,
    ) -> None:
        
        """
        Establishes a connection pool to the PostgreSQL database if not already initialized.

        The connection pool allows multiple connections to be managed efficiently.
        """
        
        if self.pool is None:
            self.pool = pool.SimpleConnectionPool (
                1, 20,  # minconn, maxconn
                host=self.host,
                user=self.db_user,
                password=self.password,
                database=self.database
            )
            
    def get_connection (
        self,
    ) -> psycopg2.extensions.connection:
        
        """
        Retrieves a database connection from the connection pool.

        If the pool is not initialized, it will establish a connection first.

        Returns:
            psycopg2.extensions.connection: A database connection from the pool.
        """
        
        if self.pool is None:
            self.connect()
        return self.pool.getconn()
    
    def release_connection (
        self, 
        connection: psycopg2.extensions.connection,
    ) -> None:
        
        """
        Releases a database connection back to the connection pool.

        Args:
            connection (psycopg2.extensions.connection): The connection to be returned to the pool.
        """
        
        self.pool.putconn(connection)

    def close_all (
        self,
    ) -> None:
        
        """
        Closes all connections in the connection pool.

        This method should be called during application shutdown to free resources.
        """
        
        if self.pool:
            self.pool.closeall()