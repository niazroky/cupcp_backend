# student_manager/serializers.py

from rest_framework import serializers
from .models import ExamRegistration

class ExamRegistrationSerializer(serializers.ModelSerializer):
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
