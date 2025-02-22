import logging

from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import UntypedToken

logger = logging.getLogger(__name__)


class Home(APIView):
    """
    Endpoint that returns a welcome message for authenticated users.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        GET method that returns a greeting message.
        """
        content = {'message': 'Hello, World!'}
        return Response(content, status=status.HTTP_200_OK)


class CSRFTokenView(APIView):
    """
    Endpoint that provides a CSRF token for the client.
    """
    authentication_classes = []  # Public endpoint; no authentication needed
    permission_classes = []      # Public endpoint; no permissions required

    def get(self, request):
        """
        GET method that returns a CSRF token.
        """
        token = get_token(request)
        return JsonResponse({'csrfToken': token}, status=status.HTTP_200_OK)


class TokenValidationView(APIView):
    """
    Endpoint for validating a JWT token.
    """
    authentication_classes = []  # Allow unauthenticated requests for token validation
    permission_classes = []      # Open endpoint for token validation

    def post(self, request):
        """
        Validate the provided JWT token and return its payload if valid.
        """
        token = request.data.get('token')
        if not token:
            return Response(
                {'detail': 'Token is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payload = UntypedToken(token)
            payload_str = str(payload)
            logger.info("Token validated successfully: %s", payload_str)
            return Response(
                {'valid': True, 'payload': payload_str},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error("Token validation failed: %s", str(e), exc_info=True)
            return Response(
                {'valid': False, 'detail': f"Token validation error: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )