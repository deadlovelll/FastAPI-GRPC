import unittest
from unittest.mock import patch, MagicMock
from fastapi.responses import JSONResponse
from post_controller import PostController

class TestPostController(unittest.TestCase):
    
    @patch('modules.base_controller.BaseController')
    @patch('pika.BlockingConnection')
    @patch('pika.ConnectionParameters')
    def setUp(self, MockConnectionParameters, MockBlockingConnection, MockBaseController):
        self.post_controller = PostController()
        self.post_controller.logger = MagicMock()
        self.mock_connection = MockBlockingConnection.return_value
        self.mock_channel = self.mock_connection.channel.return_value
        self.mock_channel.queue_declare.return_value = None

    @patch('controllers.jwt_security.JWTSecurity.validate_jwt')
    def test_create_book_success(self, mock_validate_jwt):
        book_name = "New Book"
        book_author = "Author Name"
        token = "valid_token"
        mock_validate_jwt.return_value = True
        
        response = self.post_controller.create_book(book_name, book_author, token)
        
        self.mock_channel.basic_publish.assert_called_once_with(
            exchange='', 
            routing_key='book_queue', 
            body=f"Posting Book|{book_name}|{book_author}"
        )
        self.assertEqual(response, JSONResponse({'STATUS': 'SUCCESS'}))

    @patch('controllers.jwt_security.JWTSecurity.validate_jwt')
    def test_create_book_invalid_token(self, mock_validate_jwt):
        book_name = "New Book"
        book_author = "Author Name"
        token = "invalid_token"
        mock_validate_jwt.return_value = False
        
        response = self.post_controller.create_book(book_name, book_author, token)
        
        self.assertEqual(response, JSONResponse({'STATUS': 'FAILED'}))

    @patch('controllers.jwt_security.JWTSecurity.validate_jwt')
    def test_create_book_failed_task_queue(self, mock_validate_jwt):
        book_name = "New Book"
        book_author = "Author Name"
        token = "valid_token"
        mock_validate_jwt.return_value = True
        self.mock_channel.basic_publish.side_effect = Exception("Task failed")
        
        response = self.post_controller.create_book(book_name, book_author, token)
        
        self.assertEqual(response, JSONResponse({'STATUS': 'FAILED'}))

if __name__ == '__main__':
    unittest.main()
