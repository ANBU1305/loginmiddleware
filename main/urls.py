# authentication_api/urls.py

from django.urls import path
from .views import register

urlpatterns = [
    path('register/', register, name='register'),
]