"""
Django AppConfig for the student_manager application.

Configures default settings for the student_manager app, including
primary key field type and application name.
"""

# Relative Path: student_manager/apps.py

from django.apps import AppConfig


class StudentManagerConfig(AppConfig):
    """
    Configuration class for the student_manager app.
    Sets default primary key type and identifies the app's module path.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'student_manager'