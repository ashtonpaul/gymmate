from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from metrics.models import Metric, MetricType, MetricTypeGroup

from .models import AccountUser


class BaseTestCase(APITestCase):
    # Test user accounts
    user_admin = 'admin'
    user_basic = 'user'

    def setUp(self):
        """
        Set up user for authentication to run tests
        """
        AccountUser.objects.create_user(username=self.user_admin, is_active=True, is_staff=True)
        AccountUser.objects.create_user(username=self.user_basic, is_active=True)

        self.client = APIClient()

    def authenticate(self, username=None):
        """
        Method to authenticate and switch currently logged in user
        """
        self.user = AccountUser.objects.get(username=username)
        self.client.force_authenticate(user=self.user)
        return self.user


class AccountTests(BaseTestCase):
    def test_create_user(self):
        """
        Create a profile without previous authentication
        """
        client = APIClient()
        response = client.post(reverse('user-list'), {'username': 'temp'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_other_user(self):
        """
        A user should not be able to delete another user's profile
        """
        user = self.authenticate(self.user_basic)
        self.authenticate(self.user_admin)

        response = self.client.delete(reverse('user-detail', args=(user.id,)))
        self.assertNotEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_another_user(self):
        """
        A user should not be able to update another user's profile
        """
        user = self.authenticate(self.user_basic)
        self.authenticate(self.user_admin)

        put = self.client.put(
            reverse('user-detail', args=(user.id,)),
            {'username': 'user_one', 'email': 'test@test.com'}
        )
        patch = self.client.patch(reverse('user-detail', args=(user.id,)), {'username': 'user_two'})

        self.assertNotEqual(put.status_code, status.HTTP_200_OK)
        self.assertNotEqual(patch.status_code, status.HTTP_200_OK)

    def test_metrics_cascade(self):
        """
        Metrics should be deleted when a user account is deleted
        """
        self.authenticate(self.user_basic)
        group = MetricTypeGroup.objects.create(name='height')
        type = MetricType.objects.create(group=group, name='inches', unit='in.')
        metric = Metric.objects.create(user=self.user, value='75', metric_type=type)

        self.client.delete(reverse('user-detail', args=(self.user.id,)))
        self.assertEqual(Metric.objects.count(), 0)
        self.assertRaises(Metric.DoesNotExist, lambda: Metric.objects.get(id=metric.id))