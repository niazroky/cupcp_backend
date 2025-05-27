"""
Serializers for the student_manager app.
Handles validation and transformation of ExamRegistration data.
"""

# Relative Path: student_manager/serializers.py

from rest_framework import serializers
from .models import ExamRegistration


class ExamRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for ExamRegistration model.
    Ensures that critical user-related fields remain read-only and
    provides safe handling of registration data.
    """

    class Meta:
        model = ExamRegistration
        fields = [
            "id",
            "user",
            "full_name",
            "varsity_id",
            "session",
            "phone_number",
            "payment_status",
            "payment_slip",
            "student_status",
            "courses",
            "hall_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "full_name",
            "varsity_id",
            "session",
            "phone_number",
            "created_at",
            "updated_at",
        ]
