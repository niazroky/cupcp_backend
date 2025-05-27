"""
Django URL configuration for cupcp_backend project.

This module defines URL routes for API endpoints, the admin panel,
static file serving, and a simple homepage health check.
"""

# Relative Path: cupcp_backend/urls.py

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# -----------------------------------------------------------------------------
# Health Check View
# -----------------------------------------------------------------------------
def home(request):  # Simple endpoint to verify server is running
    """
    Returns a basic HTML response indicating the server status.
    Useful for quick health checks and debugging.
    """
    return HttpResponse("<h1>Congrats, Your server is Running</h1>")

# -----------------------------------------------------------------------------
# URL Patterns
# -----------------------------------------------------------------------------
urlpatterns = [
    # Root URL: Health check / homepage
    path('', home, name='home'),

    # Admin Panel: Manage models, users, and permissions
    path('admin/', admin.site.urls),

    # Authentication Endpoints: Login, logout, token operations
    path('auth/', include('accounts.urls')),

    # Student Manager Endpoints: Exam registration and student operations
    path('student-manager/', include('student_manager.urls')),
]
