import unittest
import os
from unittest.mock import AsyncMock, patch
from fastapi_service.decorators.jwt_ssecurity.jwt_security import JWTSecurity

class TestJWTSecurity(unittest.IsolatedAsyncioTestCase):
    
    async def asyncSetUp (
        self,
    ) -> None:
        
        self.jwt_security = JWTSecurity()
        self.valid_token = 'valid_token'
        self.invalid_token = 'invalid_token'
        os.environ['JWT_VALIDATION_URL'] = 'http://mocked-url.com/validate'

    @patch('fastapi_service.decorators.jwt_ssecurity.jwt_security.aiohttp.ClientSession.post')
    async def test_validate_jwt_valid (
        self, 
        mock_post,
    ) -> None:
        
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