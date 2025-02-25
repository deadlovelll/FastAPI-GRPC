import unittest
from unittest.mock import AsyncMock, patch
from fastapi_service.lifecycle_events.startup_events.startup_handler import StartupHandler
from fastapi_service.lifecycle_events.shutdown_events.shutdown_handler import ShutdownHandler
from fastapi_service.modules.database.pool_controller.database_controller import DatabasePoolController

class TestStartupHandler(unittest.IsolatedAsyncioTestCase):
    
    """
    Unit tests for the `StartupHandler` class.

    This test suite ensures that:
    - The `StartupHandler` correctly initializes the `DatabasePoolController`.
    - The `handle_startup` method correctly triggers the startup event.
    """

    @patch.object(
        DatabasePoolController, 
        "startup_event", 
        new_callable=AsyncMock,
    )
    def test_initialization (
        self, 
        mock_startup_event,
    ) -> None:
        
        """
        Test initialization of `StartupHandler`.

        This test verifies that:
        - A `StartupHandler` instance is successfully created.
        - The `database_pool_controller` attribute is an instance of `DatabasePoolController`.
        """
        
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
        
        """
        Test handling of application startup.

        This test ensures that:
        - The `handle_startup` method correctly calls `startup_event` on the `DatabasePoolController`.
        - The startup event is awaited exactly once.
        """
        
        startup_handler = StartupHandler()
        await startup_handler.handle_startup()
        mock_startup_event.assert_awaited_once()


class TestShutdownHandler(unittest.IsolatedAsyncioTestCase):
    
    """
    Unit tests for the `ShutdownHandler` class.

    This test suite ensures that:
    - The `ShutdownHandler` correctly initializes the `DatabasePoolController`.
    - The `handle_shutdown` method correctly triggers the shutdown event.
    """

    @patch.object (
        DatabasePoolController, 
        "shutdown_event", 
        new_callable=AsyncMock,
    )
    def test_initialization (
        self, 
        mock_shutdown_event,
    ) -> None:
        
        """
        Test initialization of `ShutdownHandler`.

        This test verifies that:
        - A `ShutdownHandler` instance is successfully created.
        - The `database_pool_controller` attribute is an instance of `DatabasePoolController`.
        """
        
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
        
        """
        Test handling of application shutdown.

        This test ensures that:
        - The `handle_shutdown` method correctly calls `shutdown_event` on the `DatabasePoolController`.
        - The shutdown event is awaited exactly once.
        """
        
        shutdown_handler = ShutdownHandler()
        await shutdown_handler.handle_shutdown()
        mock_shutdown_event.assert_awaited_once()


if __name__ == "__main__":
    unittest.main()
