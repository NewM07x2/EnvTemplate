"""Pytest configuration for Django tests."""

import pytest
from django.conf import settings


@pytest.fixture(scope='session')
def django_db_setup():
    """Setup test database."""
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
