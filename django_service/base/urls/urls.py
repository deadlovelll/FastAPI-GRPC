from django.urls import path, include
from ..views.views import Home

urlpatterns = [
    path('', Home.as_view()),
]