from pathlib import Path
from datetime import timedelta
# from decouple import config, Csv


# ───────────────────────────────────────────────────────
# Project Paths and Directories
# ───────────────────────────────────────────────────────

# Define the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# ───────────────────────────────────────────────────────
# Security Settings (IMPORTANT FOR PRODUCTION)
# ───────────────────────────────────────────────────────

# Security
SECRET_KEY = 'django-insecure-xm$j2n&)3!oqk@^nmu&ayv+k9qg@fdoi8+b!1cj8==su8z3)7z'
DEBUG = True 
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '13.202.55.139', 'www.cupcp.com', 'cupcp.com']

# ───────────────────────────────────────────────────────
# Application Definition
# ───────────────────────────────────────────────────────

INSTALLED_APPS = [
    # Default Django apps for core functionalities
    'django.contrib.admin',          # Admin panel
    'django.contrib.auth',           # Authentication system
    'django.contrib.contenttypes',   # Content type framework
    'django.contrib.sessions',       # User session management
    'django.contrib.messages',       # Messaging framework
    'django.contrib.staticfiles',    # Static file handling (CSS, JS, images)

    # Third-party packages
    'corsheaders',                    # Cross-Origin Resource Sharing (CORS)
    'rest_framework',                  # Django REST framework for API development
    'rest_framework_simplejwt.token_blacklist',  # For JWT Token Blacklisting

    # Custom applications (specific to this project)
    'accounts',                         # User authentication and management
    'student_manager',                      
]

# ───────────────────────────────────────────────────────
# Middleware Configuration
# ───────────────────────────────────────────────────────

MIDDLEWARE = [
    # Handles Cross-Origin Resource Sharing (CORS) for frontend-backend communication
    'corsheaders.middleware.CorsMiddleware',

    # Security middleware for enforcing best security practices
    'django.middleware.security.SecurityMiddleware',

    # Session management middleware
    'django.contrib.sessions.middleware.SessionMiddleware',

    # Middleware to handle standard HTTP request processing
    'django.middleware.common.CommonMiddleware',

    # Protects against Cross-Site Request Forgery (CSRF) attacks
    'django.middleware.csrf.CsrfViewMiddleware',

    # Authentication middleware (manages user authentication state)
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # Middleware for handling framework-level messages (e.g., success/error messages)
    'django.contrib.messages.middleware.MessageMiddleware',

    # Prevents clickjacking attacks by controlling iframe embedding
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ───────────────────────────────────────────────────────
# Django REST Framework Configuration
# ───────────────────────────────────────────────────────

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT-based authentication
    ),
}

# ───────────────────────────────────────────────────────
# JWT (JSON Web Token) Authentication Settings
# ───────────────────────────────────────────────────────

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),

    # Rotate the refresh token and blacklist the previous one
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,

    # # Optional: limit how late you can refresh
    # "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    # "SLIDING_TOKEN_LIFETIME": timedelta(minutes=30),
    # "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}


# ───────────────────────────────────────────────────────
# Custom User Model Configuration
# ───────────────────────────────────────────────────────

# Use a custom user model from the 'accounts' app instead of Django's default user model
AUTH_USER_MODEL = 'accounts.User'

# ───────────────────────────────────────────────────────
# Teacher Email Whitelist (Role-Based Access)
# ───────────────────────────────────────────────────────

# Teacher Email Whitelist
ALLOWED_TEACHER_EMAILS = [
    'rnizam.physics@cu.ac.bd',
    'dummy1@cu.ac.bd',
    'dummy2@cu.ac.bd',
]

# ───────────────────────────────────────────────────────
# URL Configuration
# ───────────────────────────────────────────────────────

# Specifies the root URL configuration file for URL routing
ROOT_URLCONF = "cupcp_backend.urls"

# ───────────────────────────────────────────────────────
# CORS (Cross-Origin Resource Sharing) Configuration
# ───────────────────────────────────────────────────────

# Allow requests only from trusted frontend origins (e.g., React app running locally)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",   # for local development
    "https://cupcp.com",       # your live frontend domain
    "https://www.cupcp.com",   # optional, if www works
]


# Enable credentials (cookies, authorization headers) in cross-origin requests
CORS_ALLOW_CREDENTIALS = True

# ───────────────────────────────────────────────────────
# Template Configuration
# ───────────────────────────────────────────────────────

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",  # Use Django's template engine
        "DIRS": [],  # Directories where Django should look for templates (add paths if needed)
        "APP_DIRS": True,  # Enable template loading from installed apps
        "OPTIONS": {
            "context_processors": [  # Context processors make specific variables available in templates
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ───────────────────────────────────────────────────────
# WSGI Application Configuration
# ───────────────────────────────────────────────────────

# WSGI application entry point for serving the Django project
WSGI_APPLICATION = "cupcp_backend.wsgi.application"

# ───────────────────────────────────────────────────────
# Database Configuration
# ───────────────────────────────────────────────────────

# Default database configuration (using SQLite for development)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",  # Database backend engine
        "NAME": BASE_DIR / "db.sqlite3",  # Database file location
    }
}

# ───────────────────────────────────────────────────────
# Authentication & Password Validation
# ───────────────────────────────────────────────────────

# Configure password validation to enforce strong password policies
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ───────────────────────────────────────────────────────
# Internationalization & Localization Settings
# ───────────────────────────────────────────────────────

# Default language code
LANGUAGE_CODE = "en-us"

# Time zone settings
TIME_ZONE = "UTC"

# Enable Django's internationalization framework
USE_I18N = True

# Enable timezone support
USE_TZ = True


# URL path for serving static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# ───────────────────────────────────────────────────────
# Default Primary Key Field Type
# ───────────────────────────────────────────────────────

# Default auto field type for primary keys in models
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
