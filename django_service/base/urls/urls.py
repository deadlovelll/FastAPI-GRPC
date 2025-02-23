from django.urls import path
from django_service.base.views.views.views import TokenValidationView

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path (
        'api/validate-token/', 
        TokenValidationView.as_view(), 
        name='validate_token',
    ),
    path (
        'api/token/', 
        TokenObtainPairView.as_view(), 
        name='token_obtain_pair',
    ),
    path (
        'api/token/refresh/', 
        TokenRefreshView.as_view(), 
        name='token_refresh',
    ), 
]