import unittest
from unittest.mock import MagicMock, patch
from fastapi_service.controllers.book_controller.book_controller import BookController
from fastapi.responses import JSONResponse
from fastapi_service.controllers.rabbitmq_controller.rabbitmq_controller import RabbitMQController


class TestBookController(unittest.TestCase):

    def setUp(self):
        # Mocking the gRPC stub and RabbitMQ controller
        self.mock_grpc_stub = MagicMock()
        self.mock_logger = MagicMock()
        self.mock_rabbitmq_controller = MagicMock(spec=RabbitMQController)
        
        # Creating an instance of BookController
        self.controller = BookController(
            grpc_stub=self.mock_grpc_stub,
            logger=self.mock_logger,
        )
        self.controller.rabbitmq_controller = self.mock_rabbitmq_controller

    @patch.object(RabbitMQController, 'publish')
    def test_get_all_books_success(self, mock_publish):
        # Mock the gRPC response
        mock_books = ['book1', 'book2', 'book3']
        self.mock_grpc_stub.GetAllBooks.return_value = mock_books
        
        # Call the method
        response = self.controller.get_all_books()
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'STATUS': 'SUCCESS', 'BOOKS': mock_books})
        self.mock_grpc_stub.GetAllBooks.assert_called_once()
        self.mock_rabbitmq_controller.publish.assert_called_once_with('Fetching all books')
        
    @patch.object(RabbitMQController, 'publish')
    def test_get_book_by_id_success(self, mock_publish):
        # Mock the gRPC response
        book_id = 1
        mock_book = {'id': book_id, 'name': 'Test Book', 'author': 'Test Author'}
        self.mock_grpc_stub.GetBookById.return_value = mock_book
        
        # Call the method
        response = self.controller.get_book_by_id(book_id)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'STATUS': 'SUCCESS', 'BOOK': mock_book})
        self.mock_grpc_stub.GetBookById.assert_called_once_with(books_pb2.GetBookByIdRequest(book_id=book_id))
        self.mock_rabbitmq_controller.publish.assert_called_once_with(f'Fetching book by id: {book_id}')
        
    @patch.object(RabbitMQController, 'publish')
    def test_get_book_by_id_error(self, mock_publish):
        # Simulate an exception in gRPC
        book_id = 1
        self.mock_grpc_stub.GetBookById.side_effect = Exception("Error fetching book")
        
        # Call the method
        response = self.controller.get_book_by_id(book_id)
        
        # Assertions
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {'STATUS': 'FAILED', 'DETAIL': 'Error fetching book'})
        self.mock_grpc_stub.GetBookById.assert_called_once_with(books_pb2.GetBookByIdRequest(book_id=book_id))
        self.mock_rabbitmq_controller.publish.assert_called_once_with(f'Fetching book by id: {book_id}')
        
    @patch.object(RabbitMQController, 'publish')
    def test_edit_book_success(self, mock_publish):
        # Mock the success message for RabbitMQ
        book_id = 1
        book_name = "New Book"
        author = "New Author"
        
        # Call the method
        response = self.controller.edit_book(book_id, book_name, author)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'STATUS': 'SUCCESS'})
        self.mock_rabbitmq_controller.publish.assert_called_once_with(f"Editing Book|{book_id}|{book_name}|{author}")
        
    @patch.object(RabbitMQController, 'publish')
    def test_delete_book_success(self, mock_publish):
        # Mock the success message for RabbitMQ
        book_id = 1
        
        # Call the method
        response = self.controller.delete_book(book_id)
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'STATUS': 'SUCCESS'})
        self.mock_rabbitmq_controller.publish.assert_called_once_with(f"Deleting Book|{book_id}")
        
    @patch.object(RabbitMQController, 'publish')
    def test_create_book_success(self, mock_publish):
        # Mock the success message for RabbitMQ
        book_name = "New Book"
        book_author = "New Author"
        
        # Call the method
        response = self.controller.create_book(book_name, book_author)
        
        # Assertions
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'STATUS': 'SUCCESS'})
        self.mock_rabbitmq_controller.publish.assert_called_once_with(f"Posting Book|{book_name}|{book_author}")

    @patch.object(RabbitMQController, 'publish')
    def test_create_book_error(self, mock_publish):
        # Simulate an error in creating a book
        book_name = "New Book"
        book_author = "New Author"
        self.mock_rabbitmq_controller.publish.side_effect = Exception("Error publishing to RabbitMQ")
        
        # Call the method
        response = self.controller.create_book(book_name, book_author)
        
        # Assertions
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json(), {'STATUS': 'FAILED', 'DETAIL': 'Error publishing to RabbitMQ'})
        self.mock_rabbitmq_controller.publish.assert_called_once_with(f"Posting Book|{book_name}|{book_author}")


if __name__ == '__main__':
    unittest.main()
