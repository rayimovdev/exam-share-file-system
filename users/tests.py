from django.test import TestCase
from rest_framework.test import APIClient
from users.models import CustomUser

class UserViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = '/api/user/signup/'
        self.login_url = '/api/user/login/'
        self.logout_url = '/api/user/logout/'

    def test_signup(self):
        data = {
            "first_name": "Test",
            "role": "user",
            "email": "testuser@example.com",
            "password": "testpassword123"
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['success'], 'true')
        self.assertTrue(CustomUser.objects.filter(email="testuser@example.com").exists())

    def test_login(self):
        CustomUser.objects.create_user(
            first_name="Test", role="user",
            email="testlogin@example.com", password="testpassword123"
        )
        data = {
            "email": "testlogin@example.com",
            "password": "testpassword123"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], 'true')
        self.assertIn('access', response.data['data'])
        self.assertIn('refresh', response.data['data'])

    def test_logout(self):
        user = CustomUser.objects.create_user(
            first_name="Test", role="user",
            email="testlogout@example.com", password="testpassword123"
        )
        login_data = {
            "email": "testlogout@example.com",
            "password": "testpassword123"
        }
        login_response = self.client.post(self.login_url, login_data)
        refresh_token = login_response.data['data']['refresh']
        access_token = login_response.data['data']['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(self.logout_url, {"refresh": refresh_token})
        self.assertEqual(response.status_code, 205)
        self.assertEqual(response.data['success'], 'true')