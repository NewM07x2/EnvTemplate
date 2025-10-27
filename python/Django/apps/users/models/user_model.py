from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    # AbstractUserを継承することで、Djangoの認証システムと互換性を持たせます。

    def __str__(self):
        return self.username