from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .models import AccountUser


class AccountTests(APITestCase):
    def setUp(self):
        self.test_user = AccountUser.objects.create_user(username='test', password='test', is_active=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.test_user)

    def test_create_user(self):
        response = self.client.post('/users/', {'username': 'temp'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
