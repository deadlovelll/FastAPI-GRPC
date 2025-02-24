import unittest
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken

class MockUser:
    
    """
    A mock user class to simulate a user for authentication purposes in tests.
    """
    
    def __init__ (
        self, 
        id,
    ) -> None:
        
        """
        Initializes a mock user with a given user ID.

        Args:
            id: The ID of the user.
        """
        
        self.id = id

class APITestCase(unittest.TestCase):
    
    """
    Unit test case class for testing API endpoints related to authentication and token validation.
    """
    
    def setUp (
        self,
    ) -> None:
        
        """
        Sets up the test environment, including initializing the API client and tokens.
        """
        
        self.client = APIClient()
        self.valid_token = str(AccessToken.for_user(MockUser(id=1)))
        self.invalid_token = "invalid.token.string"

    def test_home_authenticated (
        self,
    ) -> None:
        
        """
        Tests the home endpoint for an authenticated user.

        Sends a GET request to the home endpoint with a valid token 
        and checks for a 200 OK status and the correct response message.
        """
        
        response = self.client.get(
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
        
        """
        Tests the home endpoint for an unauthenticated user.

        Sends a GET request to the home endpoint without authentication
        and checks for a 401 Unauthorized status.
        """
        
        response = self.client.get("/api/home/")
        self.assertEqual (
            response.status_code, 
            status.HTTP_401_UNAUTHORIZED,
        )
    
    def test_csrf_token (
        self,
    ) -> None:
        
        """
        Tests the CSRF token endpoint.

        Sends a GET request to the CSRF endpoint and checks if the CSRF token is present in the response.
        """
        
        response = self.client.get("/api/csrf/")
        self.assertEqual (
            response.status_code, 
            status.HTTP_200_OK,
        )
        self.assertIn(
            "CSRF_TOKEN", 
            response.json(),
        )
    
    @patch("base.views.base_view.base_view.BaseAPIView.logger")
    def test_token_validation_valid (
        self, 
        mock_logger,
    ) -> None:
        
        """
        Tests token validation for a valid token.

        Sends a POST request to the validate-token endpoint with a valid token 
        and checks for a 200 OK status and a valid token response.
        """
        
        response = self.client.post(
            '/api/validate-token/', 
            {'token': self.valid_token},
            format='json',
        )
        self.assertEqual (
            response.status_code, 
            status.HTTP_200_OK,
        )
        self.assertTrue(response.json()['valid'])

    @patch('base.views.base_view.base_view.BaseAPIView.logger')
    def test_token_validation_invalid (
        self, 
        mock_logger,
    ) -> None:
        
        """
        Tests token validation for an invalid token.

        Sends a POST request to the validate-token endpoint with an invalid token 
        and checks for a 400 Bad Request status and an invalid token response.
        """
        
        response = self.client.post(
            '/api/validate-token/', 
            {'token': self.invalid_token},
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
        
        """
        Tests token validation when the token is missing.

        Sends a POST request to the validate-token endpoint with no token 
        and checks for a 400 Bad Request status and the appropriate error message.
        """
        
        response = self.client.post(
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
