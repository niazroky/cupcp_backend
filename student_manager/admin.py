"""
Admin configuration for the student_manager app.

Registers ExamRegistration model with the Django admin.
"""

# Relative Path: student_manager/admin.py

from django.contrib import admin

from .models import ExamRegistration


@admin.register(ExamRegistration)
class ExamRegistrationAdmin(admin.ModelAdmin):
    """
    ModelAdmin for ExamRegistration, enabling list display and filtering.
    """
    # Fields to display in the admin list view
    list_display = (
        'user',
        'payment_status',
        'payment_slip',
        'student_status',
        'hall_name',
        'created_at'
    )

    # Filters for quick filtering in the sidebar
    list_filter = (
        'payment_status',
        'student_status',
        'hall_name'
    )

    # Searchable fields
    search_fields = (
        'user__email',
        'payment_slip',
        'hall_name'
    )

    # Readonly fields for fields managed automatically
    readonly_fields = ('created_at',)
