from modules.database.pool_controller.database_controller import DatabasePoolController

class ShutdownHandler:
    
    """
    A handler for performing shutdown tasks when the application is shutting down.

    This class encapsulates the logic for gracefully shutting down the database pool 
    and any other cleanup processes that might be needed when the application stops.

    Attributes:
        database_pool_controller (DatabasePoolController): A controller responsible for managing the database pool, 
            including handling its shutdown process.
    """

    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the ShutdownHandler and sets up the database pool controller.

        This method does not take any arguments. It initializes the database pool controller,
        which will handle the shutdown of database connections.
        """
        
        self.database_pool_controller = DatabasePoolController()

    async def handle_shutdown (
        self,
    ) -> None:
        
        """
        Handle the application shutdown process.

        This method is called when the application is shutting down, and it invokes
        the shutdown event on the `DatabasePoolController` to close any open database connections.

        Returns:
            None
        """
        
        await self.database_pool_controller.shutdown_event()
