import unittest
import grpc
from unittest.mock import MagicMock

from grpc_service.controllers.base_grpc_controller.base_grpc_controller import (
    BaseGRPCController,
)

class TestBaseGRPCController(unittest.TestCase):
    
    def setUp (
        self,
    ) -> None:
        
        """Initialize BaseGRPCController with a mocked logger."""
        
        self.logger_mock = MagicMock()
        self.controller = BaseGRPCController()
        self.controller.logger = self.logger_mock  

    def test_success_response (
        self,
    ) -> None:
        
        """Tests that `success_response` returns the response and logs success."""
        
        response = MagicMock()
        result = self.controller.success_response(response)
        
        self.logger_mock.info.assert_called_with('Response sent successfully.')
        self.assertEqual (
            result, 
            response,
        )

    def test_error_response (
        self,
    ) -> None:
        
        """Tests that `error_response` sets gRPC error context and logs the error."""
        
        context = MagicMock()
        code = grpc.StatusCode.INVALID_ARGUMENT
        message = "Invalid input"
        
        result = self.controller.error_response(context, code, message)

        self.logger_mock.error.assert_called_with(f'Error {code}: {message}')
        context.set_code.assert_called_with(code)
        context.set_details.assert_called_with(message)
        self.assertIsNone(result)  

if __name__ == "__main__":
    unittest.main()
