from fastapi_service.modules.database.pool_controller.database_controller import DatabasePoolController

class StartupHandler:
    
    """
    A handler for performing startup tasks when the application is starting up.

    This class encapsulates the logic for initializing the database pool and any other
    setup processes needed when the application starts.

    Attributes:
        database_pool_controller (DatabasePoolController): A controller responsible for managing the database pool, 
            including handling its startup process.
    """

    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the StartupHandler and sets up the database pool controller.

        This method does not take any arguments. It initializes the database pool controller,
        which will handle the startup of database connections.
        """
        
        self.database_pool_controller = DatabasePoolController()

    async def handle_startup (
        self,
    ) -> None:
        
        """
        Handle the application startup process.

        This method is called when the application is starting up, and it invokes
        the startup event on the `DatabasePoolController` to initialize the database pool.

        Returns:
            None
        """
        
        await self.database_pool_controller.startup_event()
