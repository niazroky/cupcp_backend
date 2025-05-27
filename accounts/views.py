"""
API views for the accounts app in cupcp_backend.

Provides endpoints for student/teacher registration, authentication,
logout, and user profile management with JWT integration.
"""

# Relative Path: accounts/views.py

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import (
    StudentRegistrationSerializer,
    TeacherRegistrationSerializer,
    StudentLoginSerializer,
    TeacherLoginSerializer,
    UserSerializer,
    UserDetailSerializer,
)


# -----------------------------------------------------------------------------
# Registration Views
# -----------------------------------------------------------------------------
class StudentRegisterAPIView(APIView):
    """
    Handles student registration.

    POST: Validates and creates a new student user.
    """
    def post(self, request):
        serializer = StudentRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Student registered successfully.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherRegisterAPIView(APIView):
    """
    Handles teacher registration.

    POST: Validates against email whitelist and creates a new teacher user.
    """
    def post(self, request):
        serializer = TeacherRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'message': 'Teacher registered successfully.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------------------------------------------
# Authentication Views
# -----------------------------------------------------------------------------
class StudentLoginAPIView(APIView):
    """
    Authenticates a student using varsity_id and password.

    POST: Returns JWT tokens upon successful authentication.
    """
    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
        if serializer.is_valid():
            varsity_id = serializer.validated_data['varsity_id']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(varsity_id=varsity_id, role='student')
            except User.DoesNotExist:
                return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

            if not user.check_password(password):
                return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'role': user.role,
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherLoginAPIView(APIView):
    """
    Authenticates a teacher using email and password.

    POST: Returns JWT tokens upon successful authentication.
    """
    def post(self, request):
        serializer = TeacherLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)
            if user and user.role == 'teacher':
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'role': user.role,
                    },
                    status=status.HTTP_200_OK
                )
            return Response({'error': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------------------------------------------
# Logout View
# -----------------------------------------------------------------------------
class LogoutAPIView(APIView):
    """
    Handles user logout by blacklisting the refresh token.

    POST: Blacklists the provided JWT refresh token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'detail': 'Logout successful.'}, status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------------------------------------------------------
# User Profile & Management View
# -----------------------------------------------------------------------------
class UserRegistrationAPIView(APIView):
    """
    GET: Retrieves the authenticated user's profile.
    POST: Creates a new generic user (any role).
    PUT: Updates the authenticated user's profile partially.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserDetailSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserDetailSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
