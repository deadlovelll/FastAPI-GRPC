import os
import uvicorn
from fastapi import FastAPI

from fastapi_service.routers.books import books

from fastapi_service.lifecycle_events.startup_events.startup_handler import StartupHandler
from fastapi_service.lifecycle_events.shutdown_events.shutdown_handler import ShutdownHandler
    
class AppFactory:
    
    def __init__ (
        self,
    ) -> None:
        
        self.startup_handler = StartupHandler()
        self.shutdown_handler = ShutdownHandler()
        
        self.fastapi_app = FastAPI()
        
    def __setup_lifecycle_handlers (
        self,
    ) -> None:
        
        @self.fastapi_app.on_event('startup')
        async def on_startup():
            await self.startup_handler.handle_startup()
            
        @self.fastapi_app.on_event('shutdown')
        async def on_shutdown():
            self.shutdown_handler.handle_shutdown()
    
    def __include_routers (
        self,
    ) -> None:
        
        self.fastapi_app.include_router(books.router)
    
    def create (
        self,
    ) -> FastAPI:
        
        self.__setup_lifecycle_handlers()
        self.__include_routers()
        return self.fastapi_app
    
def get_app() -> FastAPI:
    """Helper function to return an instance of the app."""
    factory = AppFactory()
    return factory.create()

app = get_app()

if __name__ == "__main__":
    uvicorn.run (
        app, 
        host=os.getenv('FASTAPI_HOST'), 
        port=int(os.getenv('FASTAPI_PORT')),
    )