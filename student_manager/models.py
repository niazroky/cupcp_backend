# student_manager/models.py

from django.db import models
from django.conf import settings

PAYMENT_STATUS_CHOICES = (
    ("Yes", "Yes"),
    ("No", "No"),
)
STUDENT_STATUS_CHOICES = (
    ("regular", "Regular"),
    ("improvement", "Improvement"),
)

class ExamRegistration(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="exam_registrations"
    )
    # Snapshot fields—never editable by student
    full_name   = models.CharField(max_length=255, editable=False)
    varsity_id  = models.CharField(max_length=8, null=True, blank=True, editable=False)
    session     = models.CharField(max_length=7, null=True, blank=True, editable=False)
    phone_number = models.CharField(max_length=11, null=True, blank=True)

    payment_status = models.CharField(max_length=3, choices=PAYMENT_STATUS_CHOICES)
    payment_slip   = models.CharField(max_length=255, null=True, blank=True, unique=True)
    student_status = models.CharField(max_length=12, choices=STUDENT_STATUS_CHOICES)
    courses        = models.JSONField()  # list of course codes

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Always refresh these from the linked user
        self.full_name  = self.user.full_name
        self.varsity_id = self.user.varsity_id
        self.session    = self.user.session
        self.phone_number    = self.user.phone_number
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ExamReg for {self.user.full_name}"
