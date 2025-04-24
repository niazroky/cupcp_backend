from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for the custom User model.
    - Ensures teachers don't have `varsity_id`
    - Provides proper user creation handling
    """
    
    list_display = ('email', 'full_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'full_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'role', 'varsity_id', 'session')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'password', 'is_staff', 'is_active')
        }),
    )

    readonly_fields = ('is_superuser',)  # Prevent accidental changes

    def get_fieldsets(self, request, obj=None):
        """
        Dynamically adjust fieldsets:
        - Hide `varsity_id` and `session` for teachers.
        """
        fieldsets = super().get_fieldsets(request, obj)
        if obj and obj.role == "teacher":
            fieldsets = (
                (None, {'fields': ('email', 'password')}),
                ('Personal Info', {'fields': ('full_name', 'role')}),
                ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
            )
        return fieldsets

admin.site.register(User, UserAdmin)
