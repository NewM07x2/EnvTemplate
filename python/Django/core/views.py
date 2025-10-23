"""Health check views."""

from django.http import JsonResponse
from django.conf import settings
import sys


def health_check(request):
    """Health check endpoint."""
    return JsonResponse({
        'status': 'healthy',
        'python_version': f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        'django_version': settings.VERSION if hasattr(settings, 'VERSION') else 'unknown',
        'debug': settings.DEBUG,
    })


def ping(request):
    """Simple ping endpoint."""
    return JsonResponse({'message': 'pong'})
