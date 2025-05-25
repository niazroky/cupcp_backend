
# student_manager/urls.py

from django.urls import path
from .views import MyExamRegistration, ExamRegistrationSummary

urlpatterns = [
    path("exam-registration/my/", MyExamRegistration.as_view(), name="my-exam-registration"),
    path("exam-registration-summary/", ExamRegistrationSummary.as_view(), name="exam-reg-summary"),
]
