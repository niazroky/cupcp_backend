# accounts\models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# ──────────────────────────────────────────────────────────────────────
# USER MANAGER
# ──────────────────────────────────────────────────────────────────────

class UserManager(BaseUserManager):
    """
    Custom user manager for handling user creation.
    """

    def create_user(self, email, full_name, role, password=None, **extra_fields):
        """Creates and returns a user with the given email, full name, and role."""
        if not email:
            raise ValueError("An email is required")
        email = self.normalize_email(email)

        user = self.model(email=email, full_name=full_name, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, password, **extra_fields):
        """Creates and returns a superuser (always assigned 'teacher' role)."""
        user = self.create_user(email=email, full_name=full_name, password=password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# ──────────────────────────────────────────────────────────────────────
# USER MODEL
# ──────────────────────────────────────────────────────────────────────

ROLE_CHOICES = (
    ('student', 'Student'),
    ('teacher', 'Teacher'),
)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for both Students and Teachers.
    - Students use `varsity_id` for login.
    - Teachers use `email` for login.
    """

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # Student-specific fields (Optional for teachers)
    varsity_id = models.CharField(
        max_length=8, unique=True, null=True, blank=True
    )  # Unique for students, blank for teachers
    session = models.CharField(max_length=50, null=True, blank=True)

    # Admin and permissions-related fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "role"]

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    def save(self, *args, **kwargs):
        """
        Ensure varsity_id is only unique for students.
        """
        if self.role == "teacher":
            self.varsity_id = None  # Ensure teachers do not have varsity_id
        super().save(*args, **kwargs)
