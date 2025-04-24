from rest_framework import serializers
from django.conf import settings
from .models import User
import re

# ──────────────────────────────────────────────────────────────────────
# REGEX PATTERNS FOR VALIDATION
# ──────────────────────────────────────────────────────────────────────

# Varsity ID must be exactly 8 digits (e.g., "20231234")
VARSITY_ID_REGEX = re.compile(r'^\d{8}$')

# Strong password requirement: 
# - At least 8 characters
# - Contains at least one uppercase letter, one lowercase letter, one number, and one special character
PASSWORD_REGEX = re.compile(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$'
)

# ─────────────────────────────────────────────────────────────────────
# STUDENT REGISTRATION SERIALIZER
# ──────────────────────────────────────────────────────────────────────

class StudentRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for student registration. 
    Validates varsity ID and password format before creating a student user.
    """
    
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'varsity_id', 'session', 'password']
    
    def validate_varsity_id(self, value):
        """Ensure varsity ID follows the required 8-digit format."""
        if not VARSITY_ID_REGEX.match(value):
            raise serializers.ValidationError("Varsity ID must be exactly 8 digits.")
        return value
    
    def validate_password(self, value):
        """Ensure password meets the security requirements."""
        if not PASSWORD_REGEX.match(value):
            raise serializers.ValidationError(
                "Password must be at least 8 characters and include uppercase, lowercase, number, and special character."
            )
        return value
    
    def create(self, validated_data):
        """Create and return a new student user instance."""
        validated_data['role'] = 'student'
        return User.objects.create_user(**validated_data)

# ──────────────────────────────────────────────────────────────────────
# TEACHER REGISTRATION SERIALIZER
# ──────────────────────────────────────────────────────────────────────

class TeacherRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for teacher registration.
    Ensures email belongs to an authorized list and password meets security standards.
    """
    
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['full_name', 'email', 'password']
    
    def validate_email(self, value):
        """Ensure the email is from the approved teacher list."""
        allowed_emails = getattr(settings, "ALLOWED_TEACHER_EMAILS", [])
        if value not in allowed_emails:
            raise serializers.ValidationError("This email is not authorized to register as a teacher.")
        return value
    
    def validate_password(self, value):
        """Ensure password meets security standards."""
        if not PASSWORD_REGEX.match(value):
            raise serializers.ValidationError(
                "Password must be at least 8 characters and include uppercase, lowercase, number, and special character."
            )
        return value
    
    def create(self, validated_data):
        """Create and return a new teacher user instance."""
        validated_data['role'] = 'teacher'
        return User.objects.create_user(**validated_data)

# ──────────────────────────────────────────────────────────────────────
# LOGIN SERIALIZERS
# ──────────────────────────────────────────────────────────────────────

# Login serializer for teachers (email-based authentication)
class TeacherLoginSerializer(serializers.Serializer):
    """
    Serializer for teacher login. 
    Requires email and password.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

# Login serializer for students (varsity ID-based authentication)
class StudentLoginSerializer(serializers.Serializer):
    """
    Serializer for student login.
    Requires varsity ID and password.
    """
    varsity_id = serializers.CharField()
    password = serializers.CharField(write_only=True)
