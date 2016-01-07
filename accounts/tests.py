from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from metrics.models import Metric, MetricType, MetricTypeGroup
from .models import AccountUser


class AccountTests(APITestCase):
    def setUp(self):
        """
        Setup the test with a default user for testing use
        """
        self.test_user = AccountUser.objects.create_user(username='test', password='test', is_active=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.test_user)

    def test_create_user(self):
        """
        Create a profile without authentication
        """
        client = APIClient()
        response = client.post(reverse('user-list'), {'username': 'temp'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_other_user(self):
        """
        A user should not be able to delete another user's profile
        """
        user_one = AccountUser.objects.create_user(username='user_one', is_active=True)
        endpoint = reverse('user-detail', args=(user_one.id,))
        response = self.client.delete(endpoint, format='json')
        self.assertNotEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_another_user(self):
        """
        A user should not be able to update another user's profile
        """
        user_one = AccountUser.objects.create_user(username='user_one', is_active=True)
        endpoint = reverse('user-detail', args=(user_one.id,))
        response = self.client.put(endpoint, {'username': 'user_one', 'email': 'test@test.com'}, format='json')
        self.assertNotEqual(response.status_code, status.HTTP_200_OK)

    def test_metrics_cascade(self):
        """
        Metrics should be deleted when a user account is deleted
        """
        group = MetricTypeGroup.objects.create(name='test_metrics_cascade')
        type = MetricType.objects.create(group=group, name='test', unit='test')
        metric = Metric.objects.create(user=self.test_user, value='1', metric_type=type)
        self.client.delete(reverse('user-detail', args=(self.test_user.id,)))
        self.assertRaises(Metric.DoesNotExist, lambda: Metric.objects.get(id=metric.id))
