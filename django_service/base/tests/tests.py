import unittest
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

class MockUser:
    
    def __init__ (
        self, 
        id,
    ) -> None:
        
        self.id = id

class APITestCase(unittest.TestCase):
    
    def setUp (
        self,
    ) -> None:
        
        self.client = APIClient()
        self.valid_token = str(AccessToken.for_user(MockUser(id=1)))
        self.invalid_token = "invalid.token.string"

    def test_home_authenticated (
        self,
    ) -> None:
        
        response = self.client.get (
            '/api/home/', 
            HTTP_AUTHORIZATION=f'Bearer {self.valid_token}',
        )
        self.assertEqual (
            response.status_code, 
            status.HTTP_200_OK,
        )
        self.assertEqual (
            response.json(), 
            {'message': 'Hello, World!'},
        )

    def test_home_unauthenticated (
        self,
    ) -> None:
        
        response = self.client.get("/api/home/")
        self.assertEqual (
            response.status_code, 
            status.HTTP_401_UNAUTHORIZED,
        )
    
    def test_csrf_token (
        self,
    ) -> None:
        
        response = self.client.get("/api/csrf/")
        self.assertEqual (
            response.status_code, 
            status.HTTP_200_OK,
        )
        self.assertIn("CSRF_TOKEN", response.json())
    
    @patch("django_service.base.views.base_view.base_view.BaseAPIView.logger")
    def test_token_validation_valid (
        self, 
        mock_logger,
    ) -> None:
        
        response = self.client.post (
            '/api/validate-token/', 
            {
                'token': self.valid_token,
            }, 
            format='json',
        )
        self.assertEqual (
            response.status_code, 
            status.HTTP_200_OK,
        )
        self.assertTrue(response.json()['valid'])

    @patch('django_service.base.views.base_view.base_view.BaseAPIView.logger')
    def test_token_validation_invalid (
        self, 
        mock_logger,
    ) -> None:
        
        response = self.client.post (
            '/api/validate-token/', 
            {
                'token': self.invalid_token,
            }, 
            format='json',
        )
        self.assertEqual (
            response.status_code, 
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertFalse(response.json()["IS_VALID"])

    def test_token_validation_missing (
        self,
    ) -> None:
        
        response = self.client.post (
            '/api/validate-token/', 
            {}, 
            format='json',
        )
        self.assertEqual (
            response.status_code, 
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual (
            response.json()['DETAIL'], 
            'Token is required.',
        )