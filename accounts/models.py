"""
Django models for the accounts app.

Defines a custom user model with role-based fields, managers,
validators, and lifecycle hooks for data integrity and formatting.
"""

# Relative Path: accounts/models.py

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


# -----------------------------------------------------------------------------
# User Manager
# -----------------------------------------------------------------------------
class UserManager(BaseUserManager):
    """
    Manager for User model, handling creation of regular users and superusers.
    """

    def create_user(
        self,
        email,
        full_name,
        role,
        phone_number=None,
        varsity_id=None,
        session=None,
        password=None,
        **extra_fields
    ):
        """
        Creates and saves a User with the given email, name, role, and optional fields.
        Validates data before saving.
        """
        if not email:
            raise ValueError("An email is required")
        email = self.normalize_email(email)

        user = self.model(
            email=email,
            full_name=full_name,
            role=role,
            phone_number=phone_number,
            varsity_id=varsity_id,
            session=session,
            **extra_fields
        )
        user.set_password(password)
        user.full_clean()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and returns a superuser with admin privileges and 'teacher' role.
        """
        extra_fields.setdefault('role', 'teacher')
        full_name = extra_fields.pop('full_name', 'Admin')
        phone_number = extra_fields.pop('phone_number', None)
        role = extra_fields.pop('role')

        user = self.create_user(
            email=email,
            full_name=full_name,
            role=role,
            phone_number=phone_number,
            varsity_id=None,
            session=None,
            password=password,
            **extra_fields
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


# -----------------------------------------------------------------------------
# Validators and Choice Definitions
# -----------------------------------------------------------------------------
VARSITY_ID_VALIDATOR = RegexValidator(
    regex=r'^\d{8}$',
    message='Varsity ID must be exactly 8 digits.'
)

PHONE_VALIDATOR = RegexValidator(
    regex=r'^\d{11}$',
    message='Phone number must be exactly 11 digits.'
)

SESSION_CHOICES = [
    (f"{yr}-{str(yr+1)[-2:]}", f"{yr}-{str(yr+1)[-2:]}")
    for yr in range(2025, 2014, -1)
]

ROLE_CHOICES = (
    ('student', 'Student'),
    ('teacher', 'Teacher'),
)

GENDER_CHOICES = (
    ('male', 'Male'),
    ('female', 'Female'),
)


# -----------------------------------------------------------------------------
# Custom User Model
# -----------------------------------------------------------------------------
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model supporting Student and Teacher roles.

    - Students authenticate via varsity_id.
    - Teachers/admins authenticate via email.
    """

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    phone_number = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        validators=[PHONE_VALIDATOR],
        help_text="11-digit contact number, required for all users."
    )
    varsity_id = models.CharField(
        max_length=8,
        unique=True,
        null=True,
        blank=True,
        validators=[VARSITY_ID_VALIDATOR],
        help_text="8-digit student ID, only for students."
    )
    session = models.CharField(
        max_length=7,
        choices=SESSION_CHOICES,
        null=True,
        blank=True,
        help_text="Academic session (e.g., 2020-21) for students."
    )
    gender = models.CharField(
        max_length=6,
        choices=GENDER_CHOICES,
        null=True,
        blank=True,
        help_text="Select gender: male=Male, female=Female (students only)"
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number']

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"

    def clean(self):
        """
        Validates role-specific constraints:
        - Students must have varsity_id, session, and gender.
        - Teachers must not have varsity_id, session, or gender.
        """
        super().clean()
        if self.role == 'student':
            if not self.varsity_id:
                raise ValidationError({'varsity_id': 'Varsity ID is required for students.'})
            if not self.session:
                raise ValidationError({'session': 'Session is required for students.'})
            if not self.gender:
                raise ValidationError({'gender': 'Gender is required for students.'})
        elif self.role == 'teacher':
            if self.varsity_id:
                raise ValidationError({'varsity_id': 'Teachers should not have a Varsity ID.'})
            if self.session:
                raise ValidationError({'session': 'Teachers should not have a session.'})
            if self.gender:
                raise ValidationError({'gender': 'Gender should not be provided for teachers.'})

    def save(self, *args, **kwargs):
        """
        Overrides save to enforce uppercase full_name and validate before persisting.
        """
        if self.full_name:
            self.full_name = self.full_name.upper()
        self.full_clean()
        super().save(*args, **kwargs)
