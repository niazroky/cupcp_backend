from django.urls import path
from .views import (
    StudentRegisterAPIView,
    TeacherRegisterAPIView,
    TeacherLoginAPIView,
    StudentLoginAPIView,
)

# ──────────────────────────────────────────────────────────────────────
# API ENDPOINTS FOR USER AUTHENTICATION & REGISTRATION
# ──────────────────────────────────────────────────────────────────────

urlpatterns = [
    # Student Registration Endpoint
    path(
        'students/register/',
        StudentRegisterAPIView.as_view(),
        name='student-register'
    ),

    # Teacher Registration Endpoint
    path(
        'teachers/register/',
        TeacherRegisterAPIView.as_view(),
        name='teacher-register'
    ),

    # Teacher Login Endpoint
    path(
        'teachers/login/',
        TeacherLoginAPIView.as_view(),
        name='teacher-login'
    ),

    # Student Login Endpoint
    path(
        'students/login/',
        StudentLoginAPIView.as_view(),
        name='student-login'
    ),
]
