import unittest
from unittest.mock import patch, MagicMock
from fastapi_service.modules.logger.logger import LoggerModule
from fastapi_service.controllers.rabbitmq_controller.rabbitmq_controller import RabbitMQController

class TestRabbitMQController(unittest.TestCase):
    
    @patch("pika.BlockingConnection")
    def setUp (
        self, 
        mock_connection,
    ) -> None:
        
        """Set up the RabbitMQController with mock dependencies."""
        
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
        
        """Test successful connection to RabbitMQ."""
        
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
        
        """Test handling of connection failure."""
        
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
        
        """Test successful message publishing."""
        
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
        
        """Test handling of message publishing failure."""
        
        self.mock_channel.basic_publish.side_effect = Exception("Publish Error")
        
        with self.assertRaises(Exception):
            self.controller.publish("Hello World")
        
        self.controller.logger.error.assert_called()
    
    def test_close_connection (
        self,
    ) -> None:
        
        """Test closing the RabbitMQ connection."""
        
        self.controller.connection.is_closed = False
        self.controller.close()
        self.controller.connection.close.assert_called_once()
        self.controller.logger.info.assert_called_with("RabbitMQ connection closed.")
    
    def test_close_already_closed (
        self,
    ) -> None:
        
        """Test closing an already closed connection."""
        
        self.controller.connection.is_closed = True
        self.controller.close()
        self.controller.connection.close.assert_not_called()

if __name__ == "__main__":
    unittest.main()
