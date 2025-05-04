from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for the custom User model.
    - Ensures teachers don't have `varsity_id` or `session`.
    - Provides proper user creation handling.
    """
    list_display = ('email', 'full_name', 'role', 'phone_number', 'gender', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    ordering = ('email',)
    search_fields = ('email', 'full_name', 'phone_number')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'role', 'phone_number', 'varsity_id', 'session', 'gender')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'phone_number', 'password1', 'password2', 'is_staff', 'is_active')
        }),
    )

    readonly_fields = ('is_superuser',)

    def get_fieldsets(self, request, obj=None):
        """
        Dynamically adjust fieldsets:
        - Hide `varsity_id` and `session` for teachers.
        """
        if not obj:
            return self.add_fieldsets
        fieldsets = [
            (None, {'fields': ('email', 'password')}),
            ('Personal Info', {
                'fields': ['full_name', 'role', 'phone_number']
                          + (['varsity_id', 'session'] if obj.role == 'student' else [])
            }),
            ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ]
        return tuple(fieldsets)


admin.site.register(User, UserAdmin)
