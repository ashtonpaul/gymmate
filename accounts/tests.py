from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from gymmate.tests import BaseTestCase
from metrics.models import Metric, MetricType, MetricTypeGroup

from .models import AccountUser


class AccountTests(BaseTestCase):
    def test_account_unicode(self):
        """
        Test unicode string represenation of the user account
        """
        user = AccountUser.objects.create_user(username='test', is_active=True)
        self.assertEqual(str(user), 'test')

    def test_create_user(self):
        """
        Create a profile without previous authentication
        """
        client = APIClient()
        response = client.post(reverse('user-list'), {'username': 'temp'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_another_user(self):
        """
        A user should not be able to create another account
        """
        self.authenticate(self.user_basic)
        response = self.client.post(
            reverse('user-list'),
            {'username': 'test'}
        )
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_user(self):
        """
        A user should be able to update their account
        """
        self.authenticate(self.user_basic)
        patch = self.client.patch(reverse('user-detail', args=(self.user.id,)), {'username': 'patched'})
        patched_user = AccountUser.objects.get(id=self.user.id)

        self.authenticate(patched_user.username)
        put = self.client.put(reverse('user-detail', args=(self.user.id,)), {'username': 'updated'})
        updated_user = AccountUser.objects.get(id=self.user.id)

        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.assertEqual(patched_user.username, 'patched')
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_user.username, 'updated')

    def test_delete_other_user(self):
        """
        A user should not be able to delete another user's profile
        """
        user = self.authenticate(self.user_admin)
        self.authenticate(self.user_basic)

        response = self.client.delete(reverse('user-detail', args=(user.id,)))
        self.assertNotEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_another_user(self):
        """
        A user should not be able to update another user's profile
        """
        user = self.authenticate(self.user_admin)
        self.authenticate(self.user_basic)

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
