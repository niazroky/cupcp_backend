"""
API Tests for Exam Registration endpoints in the student_manager app.

Covers student submission, retrieval, and teacher summary access with JWT authentication.
"""

# Relative Path: cupcp_backend/student_manager/tests/test_exam_registration_api.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from student_manager.models import ExamRegistration


class ExamRegistrationAPITests(APITestCase):
    """
    Test suite for ExamRegistration endpoints.

    Ensures correct behavior for students and teachers:
    - Students can create and retrieve their own registrations.
    - Teachers can view summary of all registrations.
    - Permissions enforced appropriately.
    """

    def setUp(self):
        """
        Initialize test users, URLs, headers, and sample data.
        """
        # Create student and teacher users
        self.student = User.objects.create_user(
            email="student1@example.com",
            full_name="Student One",
            role="student",
            phone_number="01122334455",
            varsity_id="12345678",
            session="2024-25",
            gender="female",
            password="studentpass"
        )
        self.teacher = User.objects.create_user(
            email="teacher1@example.com",
            full_name="Teacher One",
            role="teacher",
            phone_number="02233445566",
            password="teacherpass"
        )

        # Endpoint URLs
        self.register_url = reverse('my-exam-registration')
        self.summary_url = reverse('exam-reg-summary')

        # JWT auth headers
        def _token_header(user):
            token = RefreshToken.for_user(user).access_token
            return {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        self.student_header = _token_header(self.student)
        self.teacher_header = _token_header(self.teacher)

        # Valid registration payload
        self.valid_data = {
            'payment_status': 'Yes',
            'payment_slip': 'SLIP1001',
            'student_status': 'regular',
            'courses': ['PHYS-401', 'PHYS-402'],
            'hall_name': 'Alaol Hall'
        }

    # ---------------------
    # Student Registration Tests
    # ---------------------

    def test_student_registration_success(self):
        """
        Students can successfully POST exam registration data.
        """
        response = self.client.post(
            self.register_url,
            self.valid_data,
            format='json',
            **self.student_header
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reg = ExamRegistration.objects.get(user=self.student)
        self.assertEqual(reg.payment_slip, self.valid_data['payment_slip'])

    def test_student_registration_missing_payment_slip(self):
        """
        Missing payment_slip should default to blank and allow creation.
        """
        data = self.valid_data.copy()
        data.pop('payment_slip')

        response = self.client.post(
            self.register_url,
            data,
            format='json',
            **self.student_header
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reg = ExamRegistration.objects.get(user=self.student)
        self.assertTrue(reg.payment_slip in (None, ''))

    def test_student_can_retrieve_own_registration(self):
        """
        After registration, students can GET their own registration details.
        """
        # Create registration first
        self.client.post(
            self.register_url,
            self.valid_data,
            format='json',
            **self.student_header
        )

        response = self.client.get(
            self.register_url,
            format='json',
            **self.student_header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn('registration', response.data)

        reg_data = response.data['registration']
        self.assertEqual(reg_data['payment_slip'], self.valid_data['payment_slip'])
        self.assertEqual(reg_data['hall_name'], self.valid_data['hall_name'])

    def test_student_cannot_view_summary(self):
        """
        Students should receive 403 when accessing summary endpoint.
        """
        response = self.client.get(
            self.summary_url,
            format='json',
            **self.student_header
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---------------------
    # Teacher Access Tests
    # ---------------------

    def test_teacher_can_register_for_student_endpoint(self):
        """
        Teachers can POST to the registration endpoint (current behavior).
        """
        response = self.client.post(
            self.register_url,
            self.valid_data,
            format='json',
            **self.teacher_header
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            ExamRegistration.objects.filter(user=self.teacher).exists()
        )

    def test_teacher_can_view_summary(self):
        """
        Teachers can GET a summary list of all registrations.
        """
        # Create two registrations
        self.client.post(
            self.register_url,
            self.valid_data,
            format='json',
            **self.student_header
        )
        student2 = User.objects.create_user(
            email="student2@example.com",
            full_name="Student Two",
            role="student",
            phone_number="03333444555",
            varsity_id="87654321",
            session="2024-25",
            gender="male",
            password="student2pass"
        )
        header2 = {'HTTP_AUTHORIZATION': f'Bearer {RefreshToken.for_user(student2).access_token}'}
        data2 = self.valid_data.copy()
        data2['payment_slip'] = 'SLIP2002'
        self.client.post(
            self.register_url,
            data2,
            format='json',
            **header2
        )

        response = self.client.get(
            self.summary_url,
            format='json',
            **self.teacher_header
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)
        for item in response.data:
            self.assertIn('payment_status', item)
            self.assertIn('courses', item)
