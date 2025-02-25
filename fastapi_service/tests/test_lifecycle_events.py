import unittest
from unittest.mock import AsyncMock, patch
from fastapi_service.lifecycle_events.startup_events.startup_handler import StartupHandler
from fastapi_service.lifecycle_events.shutdown_events.shutdown_handler import ShutdownHandler
from fastapi_service.modules.database.pool_controller.database_controller import DatabasePoolController

class TestStartupHandler(unittest.IsolatedAsyncioTestCase):

    @patch.object(
        DatabasePoolController, 
        "startup_event", 
        new_callable=AsyncMock,
    )
    def test_initialization (
        self, 
        mock_startup_event,
    ) -> None:
        
        startup_handler = StartupHandler()
        self.assertIsInstance (
            startup_handler.database_pool_controller, 
            DatabasePoolController,
        )

    @patch.object (
        DatabasePoolController, 
        "startup_event", 
        new_callable=AsyncMock,
    )
    async def test_handle_startup (
        self, 
        mock_startup_event,
    ) -> None:
        
        startup_handler = StartupHandler()
        await startup_handler.handle_startup()
        mock_startup_event.assert_awaited_once()


class TestShutdownHandler(unittest.IsolatedAsyncioTestCase):

    @patch.object (
        DatabasePoolController, 
        "shutdown_event", 
        new_callable=AsyncMock,
    )
    def test_initialization (
        self, 
        mock_shutdown_event,
    ) -> None:
        
        shutdown_handler = ShutdownHandler()
        self.assertIsInstance (
            shutdown_handler.database_pool_controller, 
            DatabasePoolController,
        )

    @patch.object (
        DatabasePoolController, 
        "shutdown_event", 
        new_callable=AsyncMock,
    )
    async def test_handle_shutdown (
        self, 
        mock_shutdown_event,
    ) -> None:
        
        shutdown_handler = ShutdownHandler()
        await shutdown_handler.handle_shutdown()
        mock_shutdown_event.assert_awaited_once()


if __name__ == "__main__":
    unittest.main()
