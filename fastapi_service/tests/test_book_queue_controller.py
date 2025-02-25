import unittest
from unittest.mock import MagicMock, patch

from fastapi_service.controllers.book_controller.book_controller import BookController
from fastapi_service.controllers.rabbitmq_controller.rabbitmq_controller import RabbitMQController
from fastapi_service.modules.logger.logger import LoggerModule
from fastapi_service.controllers.book_queue_controller.book_queue_controller import BookQueueConsumer

class TestBookQueueConsumer(unittest.TestCase):
    
    """
    Unit tests for the `BookQueueConsumer` class.

    These tests ensure that the consumer correctly processes messages received 
    from RabbitMQ and interacts with the `BookController` and logging components.
    """

    def setUp (
        self,
    ) -> None:
        
        """
        Set up mock dependencies before each test.

        Creates mock instances of RabbitMQController, BookController, and LoggerModule,
        then initializes a `BookQueueConsumer` with these mocks.
        """
        
        self.mock_rabbit_client = MagicMock(spec=RabbitMQController)
        self.mock_book_service = MagicMock(spec=BookController)
        self.mock_logger = MagicMock(spec=LoggerModule)
        
        self.consumer = BookQueueConsumer (
            rabbit_client=self.mock_rabbit_client,
            book_service=self.mock_book_service,
            logger=self.mock_logger,
        )
        self.consumer.logger = MagicMock()

    def test_process_message_create_book (
        self,
    ) -> None:
        
        """
        Test processing a valid 'Posting Book' message.

        Ensures that the consumer correctly extracts book details from the message 
        and calls `create_book` on the book service.
        """
        
        message = 'Posting Book|New Book|New Author'
        self.consumer.process_message(message)
        self.mock_book_service.create_book.assert_called_once_with (
            'New Book', 
            'New Author',
        )

    def test_process_message_delete_book (
        self,
    ) -> None:
        
        """
        Test processing a valid 'Deleting Book' message.

        Ensures that the consumer correctly extracts the book ID and calls `delete_book`.
        """
        
        message = 'Deleting Book|1'
        self.consumer.process_message(message)
        self.mock_book_service.delete_book.assert_called_once_with(1)

    def test_process_message_edit_book (
        self,
    ) -> None:
        
        """
        Test processing a valid 'Editing Book' message.

        Ensures that the consumer correctly extracts book details and calls `update_book`.
        """
        
        message = 'Editing Book|1|Updated Book|Updated Author'
        self.consumer.process_message(message)
        self.mock_book_service.update_book.assert_called_once_with (
            1, 
            'Updated Book', 
            'Updated Author',
        )

    def test_process_message_invalid_format (
        self,
    ) -> None:
        
        """
        Test processing an invalid message format.

        Ensures that an unknown message type results in a warning log entry.
        """
        
        message = 'Invalid Message'
        self.consumer.process_message(message)
        self.consumer.logger.warning.assert_called_once_with (
            'Unknown message type: %s', 
            'Invalid Message',
        )

    def test_handle_create_book_invalid_format (
        self,
    ) -> None:
        
        """
        Test handling an invalid 'Posting Book' message format.

        Ensures that the consumer logs an error when the message lacks necessary details.
        """
        
        self.consumer._handle_create_book(['Posting Book'])
        self.consumer.logger.error.assert_called_once_with (
            'Invalid message format for "Posting Book": %s', 
            ['Posting Book'],
        )

    def test_handle_delete_book_invalid_format (
        self,
    ) -> None:
        
        """
        Test handling an invalid 'Deleting Book' message format.

        Ensures that the consumer logs an error when the message lacks a book ID.
        """
        
        self.consumer._handle_delete_book(['Deleting Book'])
        self.consumer.logger.error.assert_called_once_with (
            'Invalid message format for "Deleting Book": %s', 
            ['Deleting Book'],
        )

    def test_handle_update_book_invalid_format (
        self,
    ) -> None:
        
        """
        Test handling an invalid 'Editing Book' message format.

        Ensures that the consumer logs an error when the message lacks necessary details.
        """
        
        self.consumer._handle_update_book(['Editing Book', '1'])
        self.consumer.logger.error.assert_called_once_with (
            'Invalid message format for \'Editing Book\': %s', 
            ['Editing Book', '1'],
        )

    def test_callback (
        self,
    ) -> None:
        
        """
        Test the RabbitMQ callback function with a valid message.

        Ensures that the callback function correctly decodes the message 
        and processes it using `process_message`.
        """
        
        body = b'Posting Book|Test Book|Test Author'
        self.consumer.callback(None, None, None, body)
        self.mock_book_service.create_book.assert_called_once_with (
            'Test Book', 
            'Test Author',
        )

    @patch('fastapi_service.consumers.book_queue_consumer.BookQueueConsumer.process_message')
    def test_callback_error (
        self, 
        mock_process_message,
    ) -> None:
        
        """
        Test the RabbitMQ callback function when an error occurs.

        Simulates an exception during message processing and ensures 
        that an error is logged.
        """
        
        mock_process_message.side_effect = Exception('Test Exception')
        body = b'Invalid Message'
        self.consumer.callback(None, None, None, body)
        self.consumer.logger.error.assert_called_once()

    def test_start_consuming (
        self,
    ) -> None:
        
        """
        Test that the consumer starts consuming messages.

        Ensures that `start_consuming` correctly calls `consume` on the RabbitMQ client.
        """
        
        self.consumer.start_consuming()
        self.mock_rabbit_client.consume.assert_called_once_with(self.consumer.callback)

if __name__ == "__main__":
    unittest.main()
