import os
import uvicorn
from fastapi import FastAPI

from fastapi_service.routers.books import books
from fastapi_service.lifecycle_events.startup_events.startup_handler import StartupHandler
from fastapi_service.lifecycle_events.shutdown_events.shutdown_handler import ShutdownHandler
    
class AppFactory:
    
    """
    Factory class responsible for creating and configuring a FastAPI application.
    
    This class ensures clean initialization by handling lifecycle events, 
    including application startup and shutdown, and by including API routers.
    """
    
    def __init__ (
        self,
    ) -> None:
        
        """
        Initializes the AppFactory by setting up lifecycle handlers 
        and creating an instance of FastAPI.
        """
        
        self.startup_handler = StartupHandler()
        self.shutdown_handler = ShutdownHandler()
        
        self.fastapi_app = FastAPI()
        
    def __setup_lifecycle_handlers (
        self,
    ) -> None:
        
        """
        Sets up event handlers for application startup and shutdown.
        
        - On startup: Calls `handle_startup()` from `StartupHandler`.
        - On shutdown: Calls `handle_shutdown()` from `ShutdownHandler`.
        """
        
        @self.fastapi_app.on_event('startup')
        async def on_startup():
            
            """Handles application startup event."""
            
            await self.startup_handler.handle_startup()
            
        @self.fastapi_app.on_event('shutdown')
        async def on_shutdown():
            
            """Handles application shutdown event."""
            
            self.shutdown_handler.handle_shutdown()
    
    def __include_routers (
        self,
    ) -> None:
        
        """
        Includes all necessary API routers in the FastAPI application.
        
        This method is responsible for adding API endpoints by registering 
        routers, ensuring modular structure.
        """
        
        self.fastapi_app.include_router(books.BookEndpoints.router)
    
    def create (
        self,
    ) -> FastAPI:
        
        """
        Configures and returns a fully initialized FastAPI application.
        
        - Sets up lifecycle handlers.
        - Includes API routers.
        
        Returns:
            FastAPI: The configured FastAPI application instance.
        """
        
        self.__setup_lifecycle_handlers()
        self.__include_routers()
        return self.fastapi_app
    
def get_app() -> FastAPI:
    
    """
    Returns a new instance of the FastAPI application using AppFactory.
    
    This function ensures a clean and structured app initialization process.

    Returns:
        FastAPI: A fully configured FastAPI application instance.
    """
    
    factory = AppFactory()
    return factory.create()

app = get_app()

if __name__ == "__main__":
    uvicorn.run (
        app, 
        host=os.getenv('FASTAPI_HOST'), 
        port=int(os.getenv('FASTAPI_PORT')),
    )