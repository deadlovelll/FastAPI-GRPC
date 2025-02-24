from django.middleware.csrf import get_token
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import UntypedToken

from base.views.base_view.base_view import BaseAPIView

class Home(BaseAPIView):
    
    """
    API endpoint that returns a welcome message for authenticated users.

    This view requires JWT authentication and allows access only to authenticated users.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get (
        self, 
        request: Request,
    ) -> Response:
        
        """
        Handle GET requests to return a greeting message.

        Args:
            request: The incoming HTTP request.

        Returns:
            Response: A JSON response containing a greeting message.
        """
        
        content = {'message': 'Hello, World!'}
        return self.create_response (
            content, 
            status=status.HTTP_200_OK,
        )


class CSRFTokenView(BaseAPIView):
    
    """
    Endpoint that provides a CSRF token to clients.

    This view is public (does not require authentication).
    """

    authentication_classes = []  # Public endpoint; no authentication needed.
    permission_classes = []      # Public endpoint; no permissions required.

    def get (
        self, 
        request: Request,
    ) -> Response:
        
        """
        Handle GET requests to return a CSRF token.

        Args:
            request: The incoming HTTP request.

        Returns:
            JsonResponse: A JSON response containing the CSRF token.
        """
        
        token = get_token(request)
        return self.create_response (
            {
                'CSRF_TOKEN': token,
            }, 
            status=status.HTTP_200_OK,
        )


class TokenValidationView(BaseAPIView):
    
    """
    Endpoint for validating a provided JWT token.

    This view accepts a token via a POST request, validates it, and returns the payload if valid.
    """

    authentication_classes = []  # Allows unauthenticated requests.
    permission_classes = []      # Open endpoint for token validation.

    def post (
        self, 
        request: Request,
    ) -> Response:
        
        """
        Validate the provided JWT token and return its payload if valid.

        Expects a JSON payload with a 'token' key.

        Args:
            request: The incoming HTTP request containing the token.

        Returns:
            Response: A JSON response indicating whether the token is valid and, if valid, its payload.
        """
        
        token = request.data.get('token')
        if not token:
            return self.create_response (
                {
                    'DETAIL': 'Token is required.',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            payload = UntypedToken(token)
            payload_str = str(payload)
            
            self.logger.info (
                "Token validated successfully: %s", 
                payload_str,
            )
            
            return self.create_response (
                {
                    'valid': True, 
                    'payload': payload_str,
                },
                status=status.HTTP_200_OK,
            )
            
        except Exception as e:
            
            self.logger.error (
                "Token validation failed: %s", 
                str(e), 
                exc_info=True,
            )
            
            return self.create_response (
                {
                    'IS_VALID': False, 
                    'DETAIL': f"Token validation error: {str(e)}",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
