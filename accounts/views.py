# accounts/views.py

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    StudentRegistrationSerializer,
    TeacherRegistrationSerializer,
    TeacherLoginSerializer,
    StudentLoginSerializer
)
from .models import User

# ──────────────────────────────────────────────────────────────────────
# AUTHENTICATION API VIEWS
# ──────────────────────────────────────────────────────────────────────

class StudentRegisterAPIView(APIView):
    """
    API View for student registration.
    - Accepts student registration data.
    - Validates and saves student account.
    - Returns success message on successful registration.
    """

    def post(self, request):
        serializer = StudentRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Student registered successfully."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherRegisterAPIView(APIView):
    """
    API View for teacher registration.
    - Accepts teacher registration data.
    - Validates and saves teacher account.
    - Returns success message on successful registration.
    """

    def post(self, request):
        serializer = TeacherRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Teacher registered successfully."},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherLoginAPIView(APIView):
    """
    API View for teacher login.
    - Accepts email and password.
    - Authenticates teacher credentials.
    - Returns JWT tokens on successful authentication.
    - Token lifetime is controlled via SIMPLE_JWT settings.
    """

    def post(self, request):
        serializer = TeacherLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            # Authenticate teacher user
            user = authenticate(request, username=email, password=password)
            if user is not None and user.role == 'teacher':
                # Generate JWT tokens
                refresh = RefreshToken.for_user(user)
                access = refresh.access_token

                return Response(
                    {
                        "refresh": str(refresh),
                        "access": str(access),
                        "role": user.role
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {"error": "Invalid credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentLoginAPIView(APIView):
    """
    API View for student login.
    - Accepts varsity ID and password.
    - Authenticates student credentials.
    - Returns JWT tokens on successful authentication.
    - Token lifetime is controlled via SIMPLE_JWT settings.
    """

    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
        if serializer.is_valid():
            varsity_id = serializer.validated_data['varsity_id']
            password = serializer.validated_data['password']

            # Fetch student user by varsity ID
            try:
                user = User.objects.get(varsity_id=varsity_id, role='student')
            except User.DoesNotExist:
                return Response(
                    {"error": "Invalid credentials."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Validate password
            if not user.check_password(password):
                return Response(
                    {"error": "Invalid credentials."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(access),
                    "role": user.role
                },
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
