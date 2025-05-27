"""
Django AppConfig for the accounts application.

Configures default settings for the accounts app, including
primary key field type and application name.
"""

# Relative Path: accounts/apps.py

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Configuration for the accounts application.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'