"""Posts app configuration."""

from django.apps import AppConfig


class SampleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.sample'
    verbose_name = 'Sample '
