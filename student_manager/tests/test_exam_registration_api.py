
# student_manager/tests/test_exam_registration_api.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from student_manager.models import ExamRegistration


class ExamRegistrationAPITests(APITestCase):
    """
    Test suite for ExamRegistration endpoints in the student_manager app.
    Covers student registration, retrieval, and teacher summary access.
    """

    def setUp(self):
        """
        Set up initial users and endpoints for testing.
        Creates one student and one teacher with JWT authentication headers.
        """
        # Create a student user for exam registration tests
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
        # Create a teacher user for summary access tests
        self.teacher = User.objects.create_user(
            email="teacher1@example.com",
            full_name="Teacher One",
            role="teacher",
            phone_number="02233445566",
            password="teacherpass"
        )

        # Resolve endpoint URLs by their names
        self.register_url = reverse('my-exam-registration')
        self.summary_url = reverse('exam-reg-summary')

        # Helper function to generate JWT authentication header
        def _token_header(user):
            token = RefreshToken.for_user(user).access_token
            return {'HTTP_AUTHORIZATION': f'Bearer {token}'}

        # Prepare headers for student and teacher
        self.student_header = _token_header(self.student)
        self.teacher_header = _token_header(self.teacher)

        # Sample payload for creating an exam registration
        self.valid_data = {
            'payment_status': 'Yes',
            'payment_slip': 'SLIP1001',
            'student_status': 'regular',
            'courses': ['PHYS-401', 'PHYS-402'],
            'hall_name': 'Alaol Hall'
        }

    def test_student_registration_success(self):
        """
        Ensure a student can successfully POST exam registration data.
        Verifies HTTP 201 and correct database entry.
        """
        response = self.client.post(
            self.register_url,
            self.valid_data,
            format='json',
            **self.student_header
        )
        # Expect creation status
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reg = ExamRegistration.objects.get(user=self.student)
        # Check that the payment_slip was stored correctly
        self.assertEqual(reg.payment_slip, self.valid_data['payment_slip'])

    def test_student_registration_missing_payment_slip(self):
        """
        Verify behavior when payment_slip is omitted.
        Current implementation allows creation; payment_slip should default to blank.
        """
        incomplete = self.valid_data.copy()
        incomplete.pop('payment_slip')

        response = self.client.post(
            self.register_url,
            incomplete,
            format='json',
            **self.student_header
        )
        # Implementation permits missing payment_slip
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reg = ExamRegistration.objects.get(user=self.student)
        # Confirm default behavior for missing field
        self.assertTrue(reg.payment_slip in (None, ''))

    def test_student_can_retrieve_own_registration(self):
        """
        After registering, a student should be able to GET their own registration.
        Response structure contains a dict with 'registration' key.
        """
        # Create registration for student
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
        # Expect successful retrieval
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Response payload should include registration details
        self.assertIsInstance(response.data, dict)
        self.assertIn('registration', response.data)

        reg_data = response.data['registration']
        # Validate specific fields in the returned data
        self.assertEqual(reg_data['payment_slip'], self.valid_data['payment_slip'])
        self.assertEqual(reg_data['hall_name'], self.valid_data['hall_name'])

    def test_student_cannot_view_summary(self):
        """
        Ensure students are forbidden from accessing the summary endpoint.
        """
        response = self.client.get(
            self.summary_url,
            format='json',
            **self.student_header
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_can_register_for_student_endpoint(self):
        """
        Confirm that teachers currently can POST to the student registration endpoint.
        This may be changed in future for stricter permissions.
        """
        response = self.client.post(
            self.register_url,
            self.valid_data,
            format='json',
            **self.teacher_header
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify registration record associated with teacher
        self.assertTrue(ExamRegistration.objects.filter(user=self.teacher).exists())

    def test_teacher_can_view_summary(self):
        """
        Verify that teachers can GET a list of all registrations via summary endpoint.
        Ensures multiple records are returned correctly.
        """
        # Student one registers
        self.client.post(
            self.register_url,
            self.valid_data,
            format='json',
            **self.student_header
        )
        # Student two registers
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
        # Ensure the summary returns a list of two items
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 2)
        for item in response.data:
            # Check key fields exist in each summary entry
            self.assertIn('payment_status', item)
            self.assertIn('courses', item)
