# Custom Django App
# accounts\views.py


from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .serializers import (
    StudentRegistrationSerializer,
    TeacherRegistrationSerializer,
    StudentLoginSerializer,
    TeacherLoginSerializer,
    LogoutSerializer,
    UserSerializer,
    UserDetailSerializer,
)
from .models import User

class StudentRegisterAPIView(APIView):
    """
    API View for student registration.
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

class StudentLoginAPIView(APIView):
    """
    API View for student login (varsity_id + password).
    """
    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
        if serializer.is_valid():
            varsity_id = serializer.validated_data['varsity_id']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(varsity_id=varsity_id, role='student')
            except User.DoesNotExist:
                return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
            if not user.check_password(password):
                return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "role": user.role
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeacherLoginAPIView(APIView):
    """
    API View for teacher login (email + password).
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
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "role": user.role
                    },
                    status=status.HTTP_200_OK
                )
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Logout successful."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        

class UserRegistrationAPIView(APIView):
    """
    GET: retrieve profile
    POST: generic registration
    PUT: update profile
    """
    def get(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserDetailSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        if not request.user or not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserDetailSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


