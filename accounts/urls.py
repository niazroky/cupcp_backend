"""
URL configurations for the accounts app.

Defines authentication, registration, login, logout, and profile endpoints
using Django REST Framework and Simple JWT views.
"""

# Relative Path: accounts/urls.py

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    StudentRegisterAPIView,
    TeacherRegisterAPIView,
    StudentLoginAPIView,
    TeacherLoginAPIView,
    LogoutAPIView,
    UserRegistrationAPIView,
)

# -----------------------------------------------------------------------------
# URL Patterns
# -----------------------------------------------------------------------------
urlpatterns = [
    # Student Registration
    path(
        'students/register/',
        StudentRegisterAPIView.as_view(),
        name='student-register'
    ),

    # Teacher Registration
    path(
        'teachers/register/',
        TeacherRegisterAPIView.as_view(),
        name='teacher-register'
    ),

    # Student Login
    path(
        'students/login/',
        StudentLoginAPIView.as_view(),
        name='student-login'
    ),

    # Teacher Login
    path(
        'teachers/login/',
        TeacherLoginAPIView.as_view(),
        name='teacher-login'
    ),

    # Logout (Blacklist Refresh Token)
    path(
        'logout/',
        LogoutAPIView.as_view(),
        name='token-logout'
    ),

    # User Profile & Update (GET, PUT)
    path(
        'user/',
        UserRegistrationAPIView.as_view(),
        name='user-profile'
    ),

    # JWT Token Management
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]
