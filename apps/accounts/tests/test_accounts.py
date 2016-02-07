import datetime

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ...core.tests import BaseTestCase
from ...metrics.models import Metric, MetricType, MetricTypeGroup
from ...exercises.models import Exercise
from ...workouts.models import Routine, Progress

from ..models import AccountUser


class AccountTests(BaseTestCase):
    def test_account_unicode(self):
        """
        Test unicode string represenation of the user account
        """
        user = AccountUser.objects.create_user(username='test', is_active=True)
        self.assertEqual(str(user), 'test')

    def test_get_user(self):
        """
        Test get methods on user list and detail views
        """
        self.authenticate(self.user_basic)
        user_list = self.client.get(reverse('user-list'))
        get = self.client.get(reverse('user-detail', args=(self.user.id,)))

        self.assertEqual(user_list.status_code, status.HTTP_200_OK)
        self.assertEqual(get.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        """
        Create a profile without previous authentication
        """
        client = APIClient()
        response = client.post(
            reverse('signup-list'),
            {'email': 'test@test.com', 'password': 'temp', }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AccountUser.objects.count(), 3)

    def test_unique_user(self):
        """
        Ensure two users can't have the same user and/or email
        """
        self.authenticate(self.user_basic)

        client = APIClient()
        username = client.post(reverse('signup-list'), {'username': 'user', 'email': 'username@test.com'})
        email = client.post(reverse('signup-list'), {'username': 'user', 'email': 'email@test.com'})

        self.assertEqual(username.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(email.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(AccountUser.objects.get(id=self.user.id).username, 'user')
        self.assertEqual(AccountUser.objects.get(id=self.user.id).email, 'user@test.com')

    def test_create_another_user(self):
        """
        A non-admin user should not be able to create another account
        """
        self.authenticate(self.user_basic)
        response = self.client.post(
            reverse('user-list'),
            {'username': 'test', 'password': 'test', 'email': 'test@test.com'}
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user(self):
        """
        A user should be able to update their account
        """
        self.authenticate(self.user_basic)
        patch = self.client.patch(reverse('user-detail', args=(self.user.id,)), {'username': 'patched'})
        patched_user = AccountUser.objects.get(id=self.user.id)

        self.authenticate(patched_user.username)
        put = self.client.put(
            reverse('user-detail', args=(self.user.id,)),
            {'username': 'updated', 'password': 'test', 'email': 'update@test.com'}
        )
        updated_user = AccountUser.objects.get(id=self.user.id)

        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.assertEqual(patched_user.username, 'patched')
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_user.username, 'updated')
        self.assertEqual(AccountUser.objects.count(), 2)

    def test_delete_account(self):
        """
        A user should be able to delete their account
        """
        user = self.authenticate(self.user_basic)
        count_before_delete = AccountUser.objects.count()
        response = self.client.delete(reverse('user-detail', args=(self.user.id,)))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertRaises(AccountUser.DoesNotExist, lambda: AccountUser.objects.get(id=user.id))
        self.assertEqual(count_before_delete, 2)
        self.assertEqual(AccountUser.objects.count(), 1)

    def test_delete_other_user(self):
        """
        A user should not be able to delete another user's profile
        """
        user = self.authenticate(self.user_admin)
        self.authenticate(self.user_basic)

        response = self.client.delete(reverse('user-detail', args=(user.id,)))
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

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

    def test_routine_cascade(self):
        """
        Routines should be deleted when a user account is deleted
        """
        self.authenticate(self.user_basic)
        routine = Routine.objects.create(user=self.user, name='mondays', )
        count_before_delete = Routine.objects.count()

        self.client.delete(reverse('routine-detail', args=(routine.id,)))
        self.assertEqual(count_before_delete, 1)
        self.assertRaises(Routine.DoesNotExist, lambda: Routine.objects.get(id=routine.id))
        self.assertEqual(Routine.objects.count(), 0)

    def test_progress_cascade(self):
        """
        User progress entries should be deleted when a user account is deleted
        """
        self.authenticate(self.user_basic)
        exercise = Exercise.objects.create(name='squats', description='squat', )
        progress = Progress.objects.create(user=self.user, exercise=exercise, date=datetime.date.today())
        count_before_delete = Progress.objects.count()

        self.client.delete(reverse('progress-detail', args=(progress.id,)))
        self.assertEqual(count_before_delete, 1)
        self.assertRaises(Progress.DoesNotExist, lambda: Progress.objects.get(id=progress.id))
        self.assertEqual(Progress.objects.count(), 0)
