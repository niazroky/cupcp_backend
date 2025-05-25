
# accounts/tests/test_account_api.py

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from django.conf import settings

class AccountAPITests(APITestCase):
    def setUp(self):
        # Prepare a valid teacher email from settings for success case
        self.valid_teacher_email = settings.ALLOWED_TEACHER_EMAILS[0]
        self.student_reg_url = reverse('student-register')
        self.teacher_reg_url = reverse('teacher-register')
        self.student_login_url = reverse('student-login')
        self.teacher_login_url = reverse('teacher-login')
        self.logout_url = reverse('token_logout')
        self.refresh_url = reverse('token_refresh')

    # 1) STUDENT REGISTRATION

    def test_student_registration_success(self):
        data = {
            "full_name": "Alice Smith",
            "email": "alice@student.com",
            "varsity_id": "12345678",
            "session": "2024-25",
            "gender": "female",
            "phone_number": "01234567890",
            "password": "abc123",
            "confirm_password": "abc123"
        }
        response = self.client.post(self.student_reg_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email="alice@student.com")
        self.assertEqual(user.role, 'student')
        self.assertTrue(user.check_password("abc123"))

    def test_student_registration_invalid_varsity_id(self):
        data = {
            "full_name": "Bob Student",
            "email": "bob@student.com",
            "varsity_id": "ABC123",  # invalid
            "session": "2024-25",
            "gender": "male",
            "phone_number": "09876543210",
            "password": "pass123",
            "confirm_password": "pass123"
        }
        response = self.client.post(self.student_reg_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('varsity_id', response.data)

    def test_student_registration_password_mismatch(self):
        data = {
            "full_name": "Carol Mismatch",
            "email": "carol@student.com",
            "varsity_id": "87654321",
            "session": "2024-25",
            "gender": "female",
            "phone_number": "01122334455",
            "password": "abc123",
            "confirm_password": "xyz789"
        }
        response = self.client.post(self.student_reg_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirm_password', response.data)

    # 2) TEACHER REGISTRATION

    def test_teacher_registration_success(self):
        data = {
            "full_name": "Dr. John Teacher",
            "email": self.valid_teacher_email,
            "phone_number": "02233445566",
            "password": "teach12",
            "confirm_password": "teach12"
        }
        response = self.client.post(self.teacher_reg_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=self.valid_teacher_email)
        self.assertEqual(user.role, 'teacher')
        self.assertFalse(user.is_staff)
        self.assertTrue(user.check_password("teach12"))

    def test_teacher_registration_unauthorized_email(self):
        data = {
            "full_name": "Fake Teacher",
            "email": "notallowed@other.com",
            "phone_number": "03344556677",
            "password": "teach12",
            "confirm_password": "teach12"
        }
        response = self.client.post(self.teacher_reg_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    # 3) LOGIN

    def test_student_login_success(self):
        # first register student
        student = User.objects.create_user(
            email="login@student.com", full_name="Login Student",
            role="student", phone_number="04455667788",
            varsity_id="11223344", session="2024-25",
            gender="male", password="log123"
        )
        data = {"varsity_id": "11223344", "password": "log123"}
        response = self.client.post(self.student_login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_teacher_login_success(self):
        teacher = User.objects.create_user(
            email=self.valid_teacher_email, full_name="Login Teacher",
            role="teacher", phone_number="05566778899",
            password="teach88"
        )
        data = {"email": self.valid_teacher_email, "password": "teach88"}
        response = self.client.post(self.teacher_login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    # 4) LOGOUT (BLACKLISTING)

    def test_logout_blacklists_refresh(self):
        
        # register & login to get tokens
        user = User.objects.create_user(
            email="bl@cklist.com", full_name="Black List",
            role="student", phone_number="06677889900",
            varsity_id="22334455", session="2024-25",
            gender="female", password="blk123"
        )
        # obtain tokens via login endpoint
        login_data = {"varsity_id": "22334455", "password": "blk123"}
        login_resp = self.client.post(self.student_login_url, login_data, format='json')
        access = login_resp.data['access']
        refresh = login_resp.data['refresh']

        # set auth header for logout
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        response = self.client.post(self.logout_url, {"refresh": refresh}, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

        # Attempt to refresh with the same token should fail
        response2 = self.client.post(self.refresh_url, {"refresh": refresh}, format='json')
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)
