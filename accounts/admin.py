"""
Custom admin configuration for the User model.

Defines how user data is displayed and managed in the Django admin panel,
including dynamic field visibility based on user roles.
"""

# Relative Path: accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    """
    Custom admin panel configuration for the custom User model.
    
    Features:
    - Displays different fields depending on the user's role (e.g., only students have `varsity_id` and `session`).
    - Supports search, filtering, and ordering.
    - Customizes the add and change user forms.
    """

    # Columns shown in the admin list view
    list_display = (
        'email',
        'full_name',
        'role',
        'phone_number',
        'gender',
        'is_staff',
        'is_active',
    )

    # Filters in the sidebar
    list_filter = (
        'role',
        'is_staff',
        'is_active',
    )

    # Field used for sorting
    ordering = ('email',)

    # Fields searchable in the admin panel
    search_fields = (
        'email',
        'full_name',
        'phone_number',
    )

    # Fields displayed when editing a user
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {
            'fields': ('full_name', 'role', 'phone_number', 'varsity_id', 'session', 'gender')
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

    # Fields shown when creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'full_name',
                'role',
                'phone_number',
                'password1',
                'password2',
                'is_staff',
                'is_active',
            ),
        }),
    )

    # Prevent editing of `is_superuser` directly
    readonly_fields = ('is_superuser',)

    def get_fieldsets(self, request, obj=None):
        """
        Adjust fieldsets based on the user's role.

        Hides student-specific fields (`varsity_id`, `session`) for teachers.
        """
        if not obj:
            return self.add_fieldsets

        personal_fields = ['full_name', 'role', 'phone_number']
        if obj.role == 'student':
            personal_fields += ['varsity_id', 'session']

        return (
            (None, {'fields': ('email', 'password')}),
            ('Personal Info', {'fields': personal_fields}),
            ('Permissions', {
                'fields': (
                    'is_staff',
                    'is_active',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            }),
        )


# Register the custom user model with the custom admin configuration
admin.site.register(User, UserAdmin)
