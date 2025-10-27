from django.apps import AppConfig"""Users app configuration."""



class UsersConfig(AppConfig):from django.apps import AppConfig

    default_auto_field = 'django.db.models.BigAutoField'

    name = 'apps.users'
class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.users'
    verbose_name = 'Users'
