from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from accounts.models import AccountUser
from exercises.models import Exercise
from .models import Routine


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
