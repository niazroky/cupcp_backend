"""
Django settings for cupcp_backend project.

This configuration file uses environment variables for sensitive settings
and follows best practices for production readiness with clearly documented sections.
"""

# Relative Path: cupcp_backend/settings.py

import dj_database_url
from datetime import timedelta
from pathlib import Path

from decouple import Csv, config


# -----------------------------------------------------------------------------
# Base Directory
# -----------------------------------------------------------------------------
# Define the project root directory for building file paths dynamically.
BASE_DIR = Path(__file__).resolve().parent.parent


# -----------------------------------------------------------------------------
# Security and Debug
# -----------------------------------------------------------------------------
# SECRET_KEY: Keep this value secret in production; loaded from environment.
SECRET_KEY = config('SECRET_KEY')

# DEBUG: Disable in production for performance and security.
DEBUG = config('DEBUG', default=False, cast=bool)

# ALLOWED_HOSTS: List of hosts/domains this site can serve.
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())


# -----------------------------------------------------------------------------
# Installed Applications
# -----------------------------------------------------------------------------
INSTALLED_APPS = [
    # Django core apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'corsheaders',  # Handles CORS headers
    'rest_framework',  # API framework
    'rest_framework_simplejwt.token_blacklist',  # JWT token blacklisting

    # Local apps
    'accounts',  # Custom user management
    'student_manager',  # Student records and operations
]


# -----------------------------------------------------------------------------
# Middleware
# -----------------------------------------------------------------------------
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS support
    'django.middleware.security.SecurityMiddleware',  # Security enhancements
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session management
    'django.middleware.common.CommonMiddleware',  # Common HTTP middleware
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Auth support
    'django.contrib.messages.middleware.MessageMiddleware',  # Flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking prevention
]


# -----------------------------------------------------------------------------
# URL Configuration
# -----------------------------------------------------------------------------
ROOT_URLCONF = 'cupcp_backend.urls'


# -----------------------------------------------------------------------------
# Templates
# -----------------------------------------------------------------------------
# Define template engine settings and directories.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Add paths to custom template directories if needed
        'APP_DIRS': True,  # Auto-discover templates in app directories
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# -----------------------------------------------------------------------------
# WSGI Application
# -----------------------------------------------------------------------------
WSGI_APPLICATION = 'cupcp_backend.wsgi.application'


# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------
# DATABASE_URL: Use environment variable or default to SQLite.
DATABASE_URL = config(
    'DATABASE_URL',
    default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}"
)

DATABASES = {
    'default': dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
    )
}


# -----------------------------------------------------------------------------
# Authentication
# -----------------------------------------------------------------------------
# Custom user model for extending default Django user.
AUTH_USER_MODEL = 'accounts.User'

# Allowed teacher emails for role-based access control.
ALLOWED_TEACHER_EMAILS = config('ALLOWED_TEACHER_EMAILS', cast=Csv())


# -----------------------------------------------------------------------------
# Password Validation
# -----------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# -----------------------------------------------------------------------------
# Internationalization
# -----------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True  # Internationalization
USE_L10N = True  # Locale-aware formatting
USE_TZ = True  # Timezone support


# -----------------------------------------------------------------------------
# Static Files (CSS, JavaScript, Images)
# -----------------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'


# -----------------------------------------------------------------------------
# CORS Settings
# -----------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', cast=Csv())
CORS_ALLOW_CREDENTIALS = True


# -----------------------------------------------------------------------------
# REST Framework & JWT
# -----------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}


# -----------------------------------------------------------------------------
# Default Primary Key Field Type
# -----------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
