import psycopg2
import os 
from dotenv import load_dotenv

load_dotenv()

class Database:
    
    def __init__(self) -> None:
        self.host = os.getenv('DB_HOST')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_NAME')
        
    def __new__(cls):
        
        if cls.isinstance is None:
            cls.isinstance = super().__new__(cls)
            cls.isinstance.pool = None
            
        return cls.isinstance
    
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
            
    def release_connection(self, connection):
        
        self.pool.putconn(connection)
        
    def close_all(self):
        
        if self.pool:
            
            self.pool.closeall()