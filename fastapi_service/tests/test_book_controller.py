import asyncio
import json
import unittest
from unittest.mock import MagicMock, patch

from grpc_service.books_pb import books_pb2

from fastapi_service.controllers.book_controller.book_controller import BookController
from fastapi_service.controllers.rabbitmq_controller.rabbitmq_controller import RabbitMQController

class TestBookController(unittest.TestCase):
    
    """
    Unit tests for the `BookController` class.

    This test suite ensures that:
    - Book retrieval, creation, editing, and deletion are handled correctly.
    - gRPC and RabbitMQ interactions function as expected.
    - Proper status codes and responses are returned.
    """

    def setUp (
        self,
    ) -> None:
        
        """
        Set up mock dependencies before each test.
        """
        
        self.mock_grpc_stub = MagicMock()
        self.mock_logger = MagicMock()
        self.mock_rabbitmq_controller = MagicMock(spec=RabbitMQController)
        
        self.controller = BookController (
            grpc_stub=self.mock_grpc_stub,
            logger=self.mock_logger,
        )
        self.controller.rabbitmq_controller = self.mock_rabbitmq_controller

    @patch.object(RabbitMQController, 'publish')
    def test_get_all_books_success (
        self, 
        mock_publish,
    ) -> None:
        
        """
        Test retrieving all books successfully.

        This test ensures:
        - The correct gRPC method is called.
        - The correct response is returned.
        - The RabbitMQ message is published.
        """
        
        mock_books = ['book1', 'book2', 'book3']
        self.mock_grpc_stub.GetAllBooks.return_value = mock_books
        
        response = asyncio.run (
            self.controller.get_all_books(),
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual (
            json.loads(response.body.decode()), 
            {
                'STATUS': 'SUCCESS', 
                'BOOKS': mock_books,
            },
        )
        self.mock_grpc_stub.GetAllBooks.assert_called_once()
        self.mock_rabbitmq_controller.publish.assert_called_once_with('Fetching all books')
        
    @patch.object(RabbitMQController, 'publish')
    def test_get_book_by_id_success (
        self, 
        mock_publish,
    ) -> None:
        
        """
        Test retrieving a book by its ID.

        This test ensures:
        - The correct gRPC request is sent.
        - The correct response is returned.
        - The RabbitMQ message is published.
        """
        
        book_id = 1
        mock_book = {
            'id': book_id, 
            'name': 'Test Book', 
            'author': 'Test Author',
        }
        self.mock_grpc_stub.GetBookById.return_value = mock_book
        
        response = asyncio.run (
            self.controller.get_book_by_id(book_id),
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual (
            json.loads(response.body.decode()), 
            {
                'STATUS': 'SUCCESS', 
                'BOOK': mock_book,
            },
        )
        self.mock_grpc_stub.GetBookById.assert_called_once_with (
            books_pb2.GetBookByIdRequest(book_id=book_id)
        )
        self.mock_rabbitmq_controller.publish.assert_called_once_with(f'Fetching book by id: {book_id}')
        
    @patch.object(RabbitMQController, 'publish')
    def test_edit_book_success (
        self, 
        mock_publish,
    ) -> None:
        
        """
        Test editing a book successfully.

        This test ensures:
        - The book is updated correctly.
        - The correct response is returned.
        - The RabbitMQ message is published.
        """
        
        book_id = 1
        book_name = 'New Book'
        author = 'New Author'
        
        response = asyncio.run (
            self.controller.edit_book (
                book_id, 
                book_name, 
                author,
            )
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual (
            json.loads(response.body.decode()), 
            {
                'STATUS': 'SUCCESS',
            },
        )
        self.mock_rabbitmq_controller.publish.assert_called_once_with(f'Editing Book|{book_id}|{book_name}|{author}')
        
    @patch.object(RabbitMQController, 'publish')
    def test_delete_book_success (
        self, 
        mock_publish,
    ) -> None:
        
        """
        Test deleting a book successfully.

        This test ensures:
        - The book is deleted correctly.
        - The correct response is returned.
        - The RabbitMQ message is published.
        """
        
        book_id = 1
        
        response = asyncio.run (
            self.controller.delete_book (
                book_id,
            )
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual (
            json.loads(response.body.decode()), 
            {
                'STATUS': 'SUCCESS',
            },
        )
        self.mock_rabbitmq_controller.publish.assert_called_once_with(f'Deleting Book|{book_id}')
        
    @patch.object(RabbitMQController, 'publish')
    def test_create_book_success (
        self, 
        mock_publish,
    ) -> None:
        
        """
        Test creating a book successfully.

        This test ensures:
        - The book is created correctly.
        - The correct response is returned.
        - The RabbitMQ message is published.
        """
        
        book_name = 'New Book'
        book_author = 'New Author'
        
        response = asyncio.run (
            self.controller.create_book (
                book_name, 
                book_author,
            )
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual (
            json.loads(response.body.decode()), 
            {
                'STATUS': 'SUCCESS',
            },
        )
        self.mock_rabbitmq_controller.publish.assert_called_once_with(f'Posting Book|{book_name}|{book_author}')

    @patch.object(RabbitMQController, 'publish')
    def test_create_book_error (
        self, 
        mock_publish,
    ) -> None:
        
        """
        Test handling an error when creating a book.

        This test ensures:
        - Errors in RabbitMQ publishing are caught.
        - The correct response is returned.
        """
        
        book_name = 'New Book'
        book_author = 'New Author'
        self.mock_rabbitmq_controller.publish.side_effect = Exception('Error publishing to RabbitMQ')
        
        response = asyncio.run (
            self.controller.create_book (
                book_name, 
                book_author,
            )
        )
        
        self.assertEqual(response.status_code, 500)
        self.assertEqual (
            json.loads(response.body.decode()), 
            {
                'STATUS': 'FAILED', 
                'DETAIL': 'Error publishing to RabbitMQ',
            },
        )
        self.mock_rabbitmq_controller.publish.assert_called_once_with(f'Posting Book|{book_name}|{book_author}')


if __name__ == '__main__':
    unittest.main()
