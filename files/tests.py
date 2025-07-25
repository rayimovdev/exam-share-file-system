from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import CustomUser
from files.models import FileUpload
from django.core.files.uploadedfile import SimpleUploadedFile

class FileUploadViewsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            first_name="FileUser", role="user",
            email="fileuser@example.com", password="filepassword"
        )
        login_url = reverse('login')
        login_data = {
            "email": self.user.email,
            "password": "filepassword"
        }
        response = self.client.post('/api/user/login/', login_data)
        self.access_token = response.data['data']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_create_file_upload(self):
        url = '/api/file/create/'
        file = SimpleUploadedFile("test.txt", b"file_content")
        data = {
            "title": "Test File",
            "file": file
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['success'], 'true')
        self.assertTrue(FileUpload.objects.filter(title="Test File").exists())

    def test_list_file_upload(self):
        FileUpload.objects.create(
            title="File1", file=SimpleUploadedFile("f1.txt", b"abc"), uploaded_by=self.user
        )
        url = '/api/file/list/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], 'true')
        self.assertGreaterEqual(len(response.data['data']), 1)

    def test_detail_file_upload(self):
        file_upload = FileUpload.objects.create(
            title="File2", file=SimpleUploadedFile("f2.txt", b"abc"), uploaded_by=self.user
        )
        url = f'/api/file/detail/{file_upload.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], 'true')
        self.assertEqual(response.data['data']['title'], "File2")

    def test_update_file_upload(self):
        file_upload = FileUpload.objects.create(
            title="File3", file=SimpleUploadedFile("f3.txt", b"abc"), uploaded_by=self.user
        )
        url = f'/api/file/update/{file_upload.id}/'
        data = {"title": "File3 Updated"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], 'true')
        file_upload.refresh_from_db()
        self.assertEqual(file_upload.title, "File3 Updated")

    def test_delete_file_upload(self):
        file_upload = FileUpload.objects.create(
            title="File4", file=SimpleUploadedFile("f4.txt", b"abc"), uploaded_by=self.user
        )
        url = f'/api/file/delete/{file_upload.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], 'true')
        self.assertFalse(FileUpload.objects.filter(id=file_upload.id).exists())