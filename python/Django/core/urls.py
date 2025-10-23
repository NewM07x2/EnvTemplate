"""Health check URLs."""

from django.urls import path
from .views import health_check, ping

urlpatterns = [
    path('', health_check, name='health_check'),
    path('ping/', ping, name='ping'),
]
