from modules.database.pool_controller.database_controller import DatabasePoolController

class StartupHandler:
    
    def __init__ (
        self,
    ) -> None:
        
        self.database_pool_controller = DatabasePoolController()
        
    async def handle_startup (
        self,
    ) -> None:
        
        await self.database_pool_controller.startup_event()