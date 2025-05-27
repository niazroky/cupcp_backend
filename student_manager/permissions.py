"""
Custom permission classes for the student_manager app.
"""

# Relative Path: student_manager/permissions.py

from rest_framework import permissions


class IsTeacher(permissions.BasePermission):
    """
    Allows access only to authenticated users with the role of 'teacher'.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "role", None) == "teacher"
        )
