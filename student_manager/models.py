"""
Models for the student_manager app in cupcp_backend.

Defines the ExamRegistration model capturing exam details
and student snapshots for integrity over time.
"""

# Relative Path: student_manager/models.py

from django.conf import settings
from django.db import models


# -----------------------------------------------------------------------------
# Choice Definitions
# -----------------------------------------------------------------------------
HALL_CHOICES = [
    ('Alaol Hall', 'Alaol Hall'),
    ('A. F. Rahman Hall', 'A. F. Rahman Hall'),
    ('Shahjalal Hall', 'Shahjalal Hall'),
    ('Suhrawardy Hall', 'Suhrawardy Hall'),
    ('Shah Amanat Hall', 'Shah Amanat Hall'),
    ('Shamsun Nahar Hall', 'Shamsun Nahar Hall'),
    ('Shaheed Abdur Rab Hall', 'Shaheed Abdur Rab Hall'),
    ('Pritilata Hall', 'Pritilata Hall'),
    ('Deshnetri Begum Khaleda Zia Hall', 'Deshnetri Begum Khaleda Zia Hall'),
    ('Masterda Surja Sen Hall', 'Masterda Surja Sen Hall'),
    ('Shaheed Farhad Hossain Hall', 'Shaheed Farhad Hossain Hall'),
    ('Bijoy 24 Hall', 'Bijoy 24 Hall'),
    ('Nawab Faizunnesa Hall', 'Nawab Faizunnesa Hall'),
    ('Atish Dipankar Hall', 'Atish Dipankar Hall'),
    ('Shilpi Rashid Chowdhury Hostel', 'Shilpi Rashid Chowdhury Hostel'),
]

PAYMENT_STATUS_CHOICES = (
    ('Yes', 'Yes'),
    ('No', 'No'),
)
STUDENT_STATUS_CHOICES = (
    ('regular', 'Regular'),
    ('improvement', 'Improvement'),
)


# -----------------------------------------------------------------------------
# ExamRegistration Model
# -----------------------------------------------------------------------------
class ExamRegistration(models.Model):
    """
    Stores exam registration details for a student, capturing a snapshot
    of user data (name, ID, session) to maintain historical integrity.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='exam_registrations'
    )

    # Snapshot fields—populated from the User and not editable by students
    full_name = models.CharField(max_length=255, editable=False)
    varsity_id = models.CharField(max_length=8, null=True, blank=True, editable=False)
    session = models.CharField(max_length=7, null=True, blank=True, editable=False)
    phone_number = models.CharField(max_length=11, null=True, blank=True)

    # Exam-related fields
    payment_status = models.CharField(max_length=3, choices=PAYMENT_STATUS_CHOICES)
    payment_slip = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
        help_text='Unique identifier for the payment slip'
    )
    student_status = models.CharField(max_length=12, choices=STUDENT_STATUS_CHOICES)
    courses = models.JSONField(help_text='List of course codes registered')
    hall_name = models.CharField(
        max_length=100,
        choices=HALL_CHOICES,
        null=True,
        blank=True,
        help_text='Select the residential hall'
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Override save to refresh user snapshot before persisting.
        Ensures stored full_name, varsity_id, session, and phone_number
        always reflect the current user state.
        """
        self.full_name = self.user.full_name
        self.varsity_id = self.user.varsity_id
        self.session = self.user.session
        self.phone_number = self.user.phone_number
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Exam Registration for {self.user.full_name}"