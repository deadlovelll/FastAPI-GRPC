from fastapi_service.modules.database.model.database import Database
from fastapi_service.modules.logger.logger import LoggerModule

class DatabasePoolController:
    
    """
    Manages database connection pooling and lifecycle events.

    This class ensures the database connection is initialized at application 
    startup and properly closed during shutdown. It also provides a method 
    to retrieve the database instance.
    """
    
    def __init__ (
        self, 
        logger: LoggerModule = LoggerModule(),
    ) -> None:
        
        """
        Initializes the DatabasePoolController.

        Args:
            logger (logging.Logger): Logger instance for logging database events.
        """
        
        self.logger = logger
        self.db = None
        
    def get_db (
        self,
    ) -> Database:
        
        """
        Retrieves the database instance, initializing it if necessary.

        Returns:
            Database: The database instance.
        """
        
        if self.db is None:
            self.db = Database()
        return self.db
    
    async def startup_event (
        self,
    ) -> None:
        
        """
        Handles application startup logic.

        Initializes and starts the database connection pool.
        Logs success or failure messages accordingly.
        """
        
        self.logger.info('Starting App....')

        try:
            db = self.get_db()
            db.connect()
            self.logger.info('Database Pool Started Successfully.')
            
        except Exception as e:
            self.logger.fatal (
                f'Failed to start the database pool: {e}. Application will be stopped.', 
                exc_info=True,
            )
            
    async def shutdown_event (
        self,
    ) -> None:
        
        """
        Handles application shutdown logic.

        Ensures that all database connections are closed properly.
        Logs success or failure messages accordingly.
        """
        
        try:
            if self.db.pool:
                self.logger.info('Shutdown made successfully')
                self.db.close_all()
                
        except Exception as e:
            self.logger.fatal (
                f'Failed to close the database pool: {e}. Application will be stopped.', 
                exc_info=True,
            )