from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework_simplejwt.tokens import UntypedToken

class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
    
    def csrf_token_view(request):
        
        return JsonResponse({'csrfToken': get_token(request)})
    
class TokenValidationView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        
        token = request.data.get('token', '')
        
        if not token:
            return Response({'detail': 'Token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payload = UntypedToken(token)
            print(str(payload))
            return Response({'valid': True, 'payload': str(payload)}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'valid': False, 'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

