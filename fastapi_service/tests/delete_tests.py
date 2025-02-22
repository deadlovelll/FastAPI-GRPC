import unittest
from unittest.mock import patch, MagicMock
from fastapi.responses import JSONResponse
from delete_controller import DeleteController

class TestDeleteController(unittest.TestCase):
    
    @patch('modules.base_controller.BaseController')
    @patch('pika.BlockingConnection')
    @patch('pika.ConnectionParameters')
    def setUp(self, MockConnectionParameters, MockBlockingConnection, MockBaseController):
        self.delete_controller = DeleteController()
        self.delete_controller.logger = MagicMock()
        
        self.mock_connection = MockBlockingConnection.return_value
        self.mock_channel = self.mock_connection.channel.return_value
        self.mock_channel.queue_declare.return_value = None

    @patch('controllers.jwt_security.JWTSecurity.validate_jwt')
    def test_delete_book_success(self, mock_validate_jwt):
        book_id = 1
        token = "valid_token"
        mock_validate_jwt.return_value = True 
        
        response = self.delete_controller.delete_book(book_id, token)
        
        self.mock_channel.basic_publish.assert_called_once_with(
            exchange='', routing_key='book_queue', body=f"Deleting Book|{book_id}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, b'{"STATUS":"SUCCESS"}')

    @patch('controllers.jwt_security.JWTSecurity.validate_jwt')
    def test_delete_book_invalid_token(self, mock_validate_jwt):
        book_id = 1
        token = "invalid_token"
        mock_validate_jwt.return_value = False  
        
        response = self.delete_controller.delete_book(book_id, token)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.body, b'{"STATUS":"FAILED"}')

if __name__ == '__main__':
    unittest.main()
