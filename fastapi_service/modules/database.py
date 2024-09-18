import psycopg2
from psycopg2 import pool
from typing import Optional
import os 
from dotenv import load_dotenv

load_dotenv()

print(os.getenv('DB_USER'))
print(os.getenv('DB_USER'))

class Database:
    instance = None
    
    def __init__(self):
        
        self.host = os.getenv('DB_HOST')
        self.db_user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_NAME')
    
    def __new__(cls):
        
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.instance.pool = None
            
        return cls.instance
    
    def connect(self):
        
        if self.pool is None:
            
            self.pool = psycopg2.pool.SimpleConnectionPool(
                1, 20,  # minconn, maxconn
                host=self.host,
                user=self.db_user,
                password=self.password,
                database=self.database
            )
            
    def get_connection(self):
        
        if self.pool is None:
            self.connect()
            
        return self.pool.getconn()
    
    def release_connection(self, connection):
        
        self.pool.putconn(connection)
        
    def close_all(self):
        
        if self.pool:
            self.pool.closeall()