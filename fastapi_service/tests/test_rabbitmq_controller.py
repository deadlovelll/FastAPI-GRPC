import unittest
from unittest.mock import patch, MagicMock
from fastapi_service.modules.logger.logger import LoggerModule
from fastapi_service.controllers.rabbitmq_controller.rabbitmq_controller import RabbitMQController

class TestRabbitMQController(unittest.TestCase):
    
    """
    Unit tests for the RabbitMQController class.

    This test suite ensures that:
    - The connection to RabbitMQ is properly established.
    - Messages are published correctly.
    - Errors are logged appropriately.
    - The connection can be closed gracefully.
    """
    
    @patch("pika.BlockingConnection")
    def setUp (
        self, 
        mock_connection,
    ) -> None:
        
        """
        Set up the RabbitMQController with mock dependencies.

        This method is called before every test to create a test instance 
        of RabbitMQController with a mocked connection and logger.

        Mocks:
        - `pika.BlockingConnection`: Prevents actual RabbitMQ connections.
        - `LoggerModule.logger_initialization`: Prevents real logging.

        Attributes:
        - `self.mock_channel`: A mocked RabbitMQ channel.
        - `self.controller`: An instance of RabbitMQController for testing.
        """
        
        self.mock_channel = MagicMock()
        mock_connection.return_value.channel.return_value = self.mock_channel
        
        with patch.object (
            LoggerModule, 
            "logger_initialization", 
            return_value=MagicMock(),
        ):
            self.controller = RabbitMQController (
                host="localhost", 
                queue_name="test_queue",
            )
    
    def test_connect_success (
        self,
    ) -> None:
        
        """
        Test successful connection to RabbitMQ.

        This test verifies that:
        - The queue is declared upon connection.
        - A log message is generated indicating a successful connection.
        """
        
        self.mock_channel.queue_declare.assert_called_once_with(queue="test_queue")
        self.controller.logger.info.assert_called_with (
            'Connected to RabbitMQ on host "%s" and declared queue "%s".', 
            "localhost", 
            "test_queue",
        )
    
    @patch (
        "pika.BlockingConnection", 
        side_effect=Exception("Connection Error"),
    )
    @patch.object (
        LoggerModule, 
        "logger_initialization",
    )  
    def test_connect_failure (
        self, 
        mock_logger_init, 
        mock_connection,
    ) -> None:
        
        """
        Test handling of connection failure.

        This test ensures that when a connection error occurs:
        - The `connection` and `channel` attributes remain `None`.
        - An error message is logged.

        Mocks:
        - `pika.BlockingConnection`: Simulates a connection failure.
        - `LoggerModule.logger_initialization`: Mocks the logger to verify logging behavior.
        """
        
        mock_logger = MagicMock()
        mock_logger_init.return_value = mock_logger  

        controller = RabbitMQController (
            host="localhost", 
            queue_name="test_queue",
        )

        self.assertIsNone(controller.connection)
        self.assertIsNone(controller.channel)
        mock_logger.error.assert_called() 
    
    def test_publish_success (
        self,
    ) -> None:
        
        """
        Test successful message publishing.

        This test ensures that:
        - A message is successfully published to the RabbitMQ queue.
        - A corresponding log message is generated.
        """
        
        self.controller.publish("Hello World")
        self.mock_channel.basic_publish.assert_called_once_with (
            exchange='', 
            routing_key="test_queue", 
            body="Hello World",
        )
        self.controller.logger.info.assert_called_with (
            'Message published to queue "%s": %s', 
            "test_queue", 
            "Hello World",
        )
    
    def test_publish_failure (
        self,
    ) -> None:
        
        """
        Test handling of message publishing failure.

        This test ensures that if publishing a message fails:
        - An exception is raised.
        - An error message is logged.
        """
        
        self.mock_channel.basic_publish.side_effect = Exception("Publish Error")
        
        with self.assertRaises(Exception):
            self.controller.publish("Hello World")
        
        self.controller.logger.error.assert_called()
    
    def test_close_connection (
        self,
    ) -> None:
        
        """
        Test closing the RabbitMQ connection.

        This test verifies that:
        - The `close()` method successfully closes the connection.
        - A corresponding log message is generated.
        """
        
        self.controller.connection.is_closed = False
        self.controller.close()
        self.controller.connection.close.assert_called_once()
        self.controller.logger.info.assert_called_with("RabbitMQ connection closed.")
    
    def test_close_already_closed (
        self,
    ) -> None:
        
        """
        Test closing an already closed connection.

        This test ensures that:
        - If the connection is already closed, `close()` does nothing.
        - No redundant calls to `connection.close()` are made.
        """
        
        self.controller.connection.is_closed = True
        self.controller.close()
        self.controller.connection.close.assert_not_called()

if __name__ == "__main__":
    unittest.main()
