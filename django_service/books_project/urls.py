from django.contrib import admin
from django.urls import path, include
from base.views import Home, TokenValidationView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include("base.urls")),
    path('api/validate-token/', TokenValidationView.as_view(), name='validate_token'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
]
