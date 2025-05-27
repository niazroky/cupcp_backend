"""
Django REST Framework serializers for the accounts app.

This module defines serializers for registration, login, user operations,
with field-specific validation and clear creation workflows.
"""

# Relative Path: accounts/serializers.py

import re

from django.conf import settings
from rest_framework import serializers

from .models import User


# -----------------------------------------------------------------------------
# Regex Patterns for Validation
# -----------------------------------------------------------------------------
# Varsity ID: exactly 8 digits
VARSITY_ID_REGEX = re.compile(r'^\d{8}$')
# Password: min 6 chars, at least one lowercase and one digit
PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*\d)[A-Za-z\d]{6,}$')


# -----------------------------------------------------------------------------
# Student Registration
# -----------------------------------------------------------------------------
class StudentRegistrationSerializer(serializers.ModelSerializer):
    """
    Handles student signup, enforcing varsity ID, session, gender, and password rules.
    """
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'full_name', 'email', 'varsity_id', 'session',
            'gender', 'phone_number', 'password', 'confirm_password'
        ]

    def validate_varsity_id(self, value):
        """Ensure varsity ID is exactly 8 digits."""
        if not VARSITY_ID_REGEX.match(value):
            raise serializers.ValidationError(
                'Varsity ID must be exactly 8 digits.'
            )
        return value

    def validate_password(self, value):
        """Ensure password meets complexity requirements."""
        if not PASSWORD_REGEX.match(value):
            raise serializers.ValidationError(
                'Password must be at least 6 characters, include a lowercase letter and a number.'
            )
        return value

    def validate(self, data):
        """Cross-field validation for password confirmation."""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'Passwords do not match.'
            })
        return data

    def create(self, validated_data):
        """
        Create a student user, removing confirmation field before user creation.
        """
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        validated_data['role'] = 'student'
        return User.objects.create_user(
            password=password,
            **validated_data
        )


# -----------------------------------------------------------------------------
# Teacher Registration
# -----------------------------------------------------------------------------
class TeacherRegistrationSerializer(serializers.ModelSerializer):
    """
    Handles teacher signup, enforcing allowed email whitelist and password rules.
    """
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'full_name', 'email', 'phone_number', 'password', 'confirm_password'
        ]

    def validate_email(self, value):
        """Ensure email is in allowed teacher whitelist."""
        allowed = getattr(settings, 'ALLOWED_TEACHER_EMAILS', [])
        if value not in allowed:
            raise serializers.ValidationError(
                'Email not authorized for teacher registration.'
            )
        return value

    def validate_password(self, value):
        """Ensure password meets complexity requirements."""
        if not PASSWORD_REGEX.match(value):
            raise serializers.ValidationError(
                'Password must be at least 6 characters, include a lowercase letter and a number.'
            )
        return value

    def validate(self, data):
        """Cross-field validation for password confirmation."""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({
                'confirm_password': 'Passwords do not match.'
            })
        return data

    def create(self, validated_data):
        """
        Create a teacher user, removing confirmation field before user creation.
        """
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        validated_data['role'] = 'teacher'
        return User.objects.create_user(
            password=password,
            **validated_data
        )


# -----------------------------------------------------------------------------
# Login and Logout Serializers
# -----------------------------------------------------------------------------
class StudentLoginSerializer(serializers.Serializer):
    varsity_id = serializers.CharField()
    password = serializers.CharField(write_only=True)


class TeacherLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        return attrs


# -----------------------------------------------------------------------------
# General User Serializers
# -----------------------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing and updating user details, with password handling.
    """
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'role', 'phone_number',
            'varsity_id', 'session', 'gender', 'password', 'confirm_password'
        ]
        read_only_fields = ['id']

    def validate(self, data):
        """Ensure passwords match and meet complexity requirements."""
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError(
                {'confirm_password': 'Passwords do not match.'}
            )
        if not PASSWORD_REGEX.match(data['password']):
            raise serializers.ValidationError(
                {'password': 'Password must be at least 6 characters, include a lowercase letter and a number.'}
            )
        return data

    def create(self, validated_data):
        """
        Create a new user and remove confirmation field before saving.
        """
        validated_data.pop('confirm_password')
        password = validated_data.pop('password')
        return User.objects.create_user(
            password=password,
            **validated_data
        )


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving user details; read-only.
    """
    class Meta:
        model = User
        fields = [
            'id', 'email', 'full_name', 'role', 'phone_number',
            'varsity_id', 'session', 'gender'
        ]
        read_only_fields = fields
