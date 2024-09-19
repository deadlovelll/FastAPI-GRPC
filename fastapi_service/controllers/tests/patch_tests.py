import unittest
from unittest.mock import patch, MagicMock
from fastapi.responses import JSONResponse
from patch_controller import PatchController

class TestPatchController(unittest.TestCase):
    
    @patch('modules.base_controller.BaseController')
    @patch('pika.BlockingConnection')
    @patch('pika.ConnectionParameters')
    def setUp(self, MockConnectionParameters, MockBlockingConnection, MockBaseController):
        self.patch_controller = PatchController()
        self.patch_controller.logger = MagicMock()
        self.mock_connection = MockBlockingConnection.return_value
        self.mock_channel = self.mock_connection.channel.return_value
        self.mock_channel.queue_declare.return_value = None

    @patch('controllers.jwt_security.JWTSecurity.validate_jwt')
    def test_editbook_success(self, mock_validate_jwt):
        book_id = 1
        book_name = "New Book Name"
        author = "Author Name"
        token = "valid_token"
        mock_validate_jwt.return_value = True
        
        response = self.patch_controller.editbook(book_id, book_name, author, token)
        
        self.mock_channel.basic_publish.assert_called_once_with(
            exchange='', 
            routing_key='book_queue', 
            body=f"Editing Book|{book_id}|{book_name}|{author}"
        )
        self.assertEqual(response, JSONResponse({'STATUS': 'SUCCESS'}))

    @patch('controllers.jwt_security.JWTSecurity.validate_jwt')
    def test_editbook_invalid_token(self, mock_validate_jwt):
        book_id = 1
        book_name = "New Book Name"
        author = "Author Name"
        token = "invalid_token"
        mock_validate_jwt.return_value = False
        
        response = self.patch_controller.editbook(book_id, book_name, author, token)
        
        self.assertEqual(response, JSONResponse({'STATUS': 'FAILED'}))

    @patch('controllers.jwt_security.JWTSecurity.validate_jwt')
    def test_editbook_failed_task_queue(self, mock_validate_jwt):
        book_id = 1
        book_name = "New Book Name"
        author = "Author Name"
        token = "valid_token"
        mock_validate_jwt.return_value = True
        self.mock_channel.basic_publish.side_effect = Exception("Task failed")
        
        response = self.patch_controller.editbook(book_id, book_name, author, token)
        
        self.assertEqual(response, JSONResponse({'STATUS': 'FAILED'}))

if __name__ == '__main__':
    unittest.main()
