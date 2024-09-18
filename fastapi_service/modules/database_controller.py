from .database import Database
import logging

class DatabasePoolController:
    
    def __init__(self, logger: logging.Logger) -> None:
        
        self.logger = logger
        self.db = None
        
    def get_db(self) -> Database:
        
        if self.db is None:
            
            self.db = Database()
            
        return self.db
    
    async def startup_event(self) -> None:
        
        self.logger.info('Starting App....')
        
        try:
            
            db = self.get_db()
            
            db.connect()
            
            self.logger.info('Database Pool Started Successfuly.')
            
        except Exception as e:
            
            self.logger.fatal(f'Failed to start the database pool: {e}. Application would be stopped.', exc_info=True)
            
    async def shutdown_event(self) -> None:
        
        try:
            
            if self.db.pool:
                
                self.logger.info('Shutdown made successfully')
                
                self.db.close_all()
                
        except Exception as e:
            
            self.logger.fatal(f'Failed to close the database pool: {e}. Application would be stopped.', exc_info=True)