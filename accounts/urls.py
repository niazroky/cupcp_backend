
# accounts/urls.py

from django.urls import path
from .views import (
    StudentRegisterAPIView,
    TeacherRegisterAPIView,
    StudentLoginAPIView,
    TeacherLoginAPIView,
    LogoutAPIView,
    UserRegistrationAPIView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

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

    # Student Login Endpoint
    path(
        'students/login/',
        StudentLoginAPIView.as_view(),
        name='student-login'
    ),

    # Teacher Login Endpoint
    path(
        'teachers/login/',
        TeacherLoginAPIView.as_view(),
        name='teacher-login'
    ),

    # Logout Endpoint
    path('logout/', 
         LogoutAPIView.as_view(), 
         name='token_logout'
    ),

    # User Profile & Generic Registration/Update Endpoint
    path(
        'user/',
        UserRegistrationAPIView.as_view(),
        name='user-profile'
    ),

    # Get Token Pair
    path('api/token/', 
         TokenObtainPairView.as_view(), 
         name='token_obtain_pair'
    ),

    # Get Refresh Token
    path('api/token/refresh/', 
         TokenRefreshView.as_view(), 
         name='token_refresh'
    ),
]
