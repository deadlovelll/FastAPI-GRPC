from modules.database.pool_controller.database_controller import DatabasePoolController

class ShutdownHandler:
    
    def __init__ (
        self,
    ) -> None:
        
        self.database_pool_controller = DatabasePoolController()
        
    async def handle_shutdown (
        self,
    ) -> None:
        
        await self.database_pool_controller.shutdown_event()