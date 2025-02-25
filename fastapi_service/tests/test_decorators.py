import unittest
import os
from unittest.mock import AsyncMock, patch
from fastapi_service.decorators.jwt_ssecurity.jwt_security import JWTSecurity

class TestJWTSecurity(unittest.IsolatedAsyncioTestCase):
    
    """
    Unit tests for the `JWTSecurity` class.

    This test suite ensures that:
    - JWT validation works correctly for valid and invalid tokens.
    - The `jwt_required` decorator correctly enforces authentication.
    """
    
    async def asyncSetUp (
        self,
    ) -> None:
        
        """
        Set up the test environment.

        This method initializes an instance of `JWTSecurity` and sets up mock values for valid and invalid tokens.
        It also configures an environment variable for the JWT validation URL.
        """
        
        self.jwt_security = JWTSecurity()
        self.valid_token = 'valid_token'
        self.invalid_token = 'invalid_token'
        os.environ['JWT_VALIDATION_URL'] = 'http://mocked-url.com/validate'

    @patch('fastapi_service.decorators.jwt_ssecurity.jwt_security.aiohttp.ClientSession.post')
    async def test_validate_jwt_valid (
        self, 
        mock_post,
    ) -> None:
        
        """
        Test validation of a valid JWT token.

        This test verifies that:
        - The `validate_jwt` method correctly calls the external validation endpoint.
        - A valid token returns `True`.
        """
        
        mock_response = AsyncMock()
        mock_response.json.return_value = {'valid': True}
        mock_post.return_value.__aenter__.return_value = mock_response
        
        result = await self.jwt_security.validate_jwt(self.valid_token)
        self.assertTrue(result)
        mock_post.assert_called_once_with (
            'http://mocked-url.com/validate', 
            json={'token': self.valid_token},
        )
    
    @patch('fastapi_service.decorators.jwt_ssecurity.jwt_security.aiohttp.ClientSession.post')
    async def test_validate_jwt_invalid (
        self, 
        mock_post,
    ) -> None:
        
        """
        Test validation of an invalid JWT token.

        This test ensures that:
        - An invalid token correctly returns `False`.
        """
        
        mock_response = AsyncMock()
        mock_response.json.return_value = {'valid': False}
        mock_post.return_value.__aenter__.return_value = mock_response
        
        result = await self.jwt_security.validate_jwt(self.invalid_token)
        self.assertFalse(result)

    @patch.object (
        JWTSecurity, 
        'validate_jwt', 
        new_callable=AsyncMock,
    )
    async def test_jwt_required_decorator_valid (
        self, 
        mock_validate_jwt,
    ) -> None:
        
        """
        Test the `jwt_required` decorator with a valid token.

        This test verifies that:
        - If a valid token is provided, the protected function executes successfully.
        - The `validate_jwt` method is called with the correct token.
        """
        
        mock_validate_jwt.return_value = True
        
        @self.jwt_security.jwt_required
        async def protected_endpoint(token):
            return 'Success'

        result = await protected_endpoint(token=self.valid_token)
        self.assertEqual(result, 'Success')
        mock_validate_jwt.assert_called_once_with(self.valid_token)
    
    @patch.object (
        JWTSecurity, 
        'validate_jwt', 
        new_callable=AsyncMock,
    )
    async def test_jwt_required_decorator_invalid (
        self, 
        mock_validate_jwt,
    ) -> None:
        
        """
        Test the `jwt_required` decorator with an invalid token.

        This test ensures that:
        - If an invalid token is provided, a `PermissionError` is raised.
        - The error message is 'Invalid JWT token.'.
        - The `validate_jwt` method is called with the correct token.
        """
        
        mock_validate_jwt.return_value = False
        
        @self.jwt_security.jwt_required
        async def protected_endpoint(token):
            return 'Success'

        with self.assertRaises(PermissionError) as context:
            await protected_endpoint(token=self.invalid_token)
        
        self.assertEqual (
            str(context.exception), 
            'Invalid JWT token.',
        )
        mock_validate_jwt.assert_called_once_with(self.invalid_token)

    async def test_jwt_required_decorator_missing_token (
        self,
    ) -> None:
        
        """
        Test the `jwt_required` decorator when no token is provided.

        This test ensures that:
        - If no token is provided to the decorated function, a `ValueError` is raised.
        - The error message is 'JWT token is required.'.
        """
        
        @self.jwt_security.jwt_required
        async def protected_endpoint(token):
            return 'Success'
        
        with self.assertRaises(ValueError) as context:
            await protected_endpoint()
        
        self.assertEqual (
            str(context.exception), 
            'JWT token is required.',
        )

if __name__ == '__main__':
    unittest.main()