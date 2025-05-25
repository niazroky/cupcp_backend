
# student_manager/permissions.py

from rest_framework import permissions

class IsTeacher(permissions.BasePermission):
    """
    Custom permission to allow only teacher users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'teacher'
