

# accounts/serializers.py

from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from .models import User
import re

# ─────────────────────────────────────────────────────────────────────
# REGEX PATTERNS FOR VALIDATION
# ─────────────────────────────────────────────────────────────────────

VARSITY_ID_REGEX = re.compile(r'^\d{8}$')
PASSWORD_REGEX = re.compile(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$'
)

# ─────────────────────────────────────────────────────────────────────
# STUDENT & TEACHER REGISTRATION SERIALIZERS
# ─────────────────────────────────────────────────────────────────────

class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'varsity_id', 'session', 'gender', 'phone_number', 'password', 'confirm_password']

    def validate_varsity_id(self, value):
        if not VARSITY_ID_REGEX.match(value):
            raise serializers.ValidationError("Varsity ID must be exactly 8 digits.")
        return value


    def validate_password(self, value):
        if not PASSWORD_REGEX.match(value):
            raise serializers.ValidationError(
                "Password must be at least 8 characters and include uppercase, lowercase, number, and special character."
            )
        validate_password(value)
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': "Passwords do not match."
            })
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        validated_data['role'] = 'student'
        return User.objects.create_user(
            password=password,
            **validated_data
        )

class TeacherRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'phone_number', 'password', 'confirm_password']

    def validate_email(self, value):
        allowed = getattr(settings, 'ALLOWED_TEACHER_EMAILS', [])
        if value not in allowed:
            raise serializers.ValidationError("Email not authorized for teacher registration.")
        return value

    def validate_password(self, value):
        if not PASSWORD_REGEX.match(value):
            raise serializers.ValidationError(
                "Password must be at least 8 characters and include uppercase, lowercase, number, and special character."
            )
        validate_password(value)
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': "Passwords do not match."
            })
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        validated_data['role'] = 'teacher'
        return User.objects.create_user(
            password=password,
            **validated_data
        )

# ─────────────────────────────────────────────────────────────────────
# LOGIN SERIALIZERS
# ─────────────────────────────────────────────────────────────────────

class StudentLoginSerializer(serializers.Serializer):
    varsity_id = serializers.CharField()
    password = serializers.CharField(write_only=True)

class TeacherLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

# ─────────────────────────────────────────────────────────────────────
# LOGOUT SERIALIZERS
# ─────────────────────────────────────────────────────────────────────

class LogoutSerializer(serializers.Serializer):
    """
    Accepts a refresh token and validates that it is well-formed.
    """
    refresh = serializers.CharField()

    def validate(self, attrs):
        return attrs
    
# ─────────────────────────────────────────────────────────────────────
# PROFILE SERIALIZERS
# ─────────────────────────────────────────────────────────────────────

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'role', 'phone_number', 'varsity_id', 'session',
            'gender', 'password', 'confirm_password'
        ]
        read_only_fields = ['id']

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
        validate_password(data['password'], user=User(**data))
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        return User.objects.create_user(
            password=password,
            **validated_data
        )

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            validated_data.pop('confirm_password', None)
            instance.set_password(password)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'role', 'phone_number', 'varsity_id', 'session', 'gender']
        read_only_fields = fields
