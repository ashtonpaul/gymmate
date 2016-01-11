from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from accounts.models import AccountUser
from exercises.models import Exercise
from .models import DayOfWeek, Routine


class BaseTestCase(APITestCase):
    def setUp(self):
        """
        Set up user for authentication to run tests
        """
        self.test_user = AccountUser.objects.create_user(username='test', password='test', is_active=True,
                                                         is_staff=True, is_superuser=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.test_user)

    def create_non_admin_user(self):
        """
        Create a non admin user for use in various tests
        """
        self.non_admin_user = AccountUser.objects.create_user(username='non_admin', password='test', is_active=True, )
        self.client.force_authenticate(user=self.non_admin_user)


class DayOfWeekTest(BaseTestCase):
    def test_add_day(self):
        response = self.client.post(reverse('dayofweek-list'), {'day': 'monday'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DayOfWeek.objects.count(), 1)
        self.assertEqual(DayOfWeek.objects.get().day, 'monday')

    def test_delete_day(self):
        day = DayOfWeek.objects.create(day='monday')
        response = self.client.delete(reverse('dayofweek-detail', args=(day.id, )))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DayOfWeek.objects.count(), 0)
        self.assertRaises(DayOfWeek.DoesNotExist, lambda: DayOfWeek.objects.get(id=day.id))

    def test_update_day(self):
        day = DayOfWeek.objects.create(day='monday')
        self.client.put(reverse('dayofweek-detail', args=(day.id, )), {'day': 'tuesday'})
        day_updated = DayOfWeek.objects.get(id=day.id)
        self.assertEqual(day_updated.day, 'tuesday')
        self.assertEqual(DayOfWeek.objects.count(), 1)

    def test_permissions(self):
        day = DayOfWeek.objects.create(day='sunday')
        self.create_non_admin_user()
        add = self.client.post(reverse('dayofweek-list'), {'day':'monday'})
        delete = self.client.delete(reverse('dayofweek-detail', args=(day.id, )))
        put = self.client.put(reverse('dayofweek-detail', args=(day.id, )), {'day': 'tuesday'})

        self.assertEqual(add.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(put.status_code, status.HTTP_403_FORBIDDEN)


class RoutineTest(BaseTestCase):
    def test_add_routine(self):
        exercise = Exercise.objects.create(name='squats', description='squat')
        response = self.client.post(
            reverse('routine-list'),
            {'name': 'mondays', 'exercises': '%d' % exercise.id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Routine.objects.count(), 1)
        self.assertEqual(Routine.objects.get().name, 'mondays')
