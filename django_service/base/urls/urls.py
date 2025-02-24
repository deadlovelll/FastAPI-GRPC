from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from base.views.views.views import TokenValidationView

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