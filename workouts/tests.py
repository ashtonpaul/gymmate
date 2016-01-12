import datetime

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from accounts.models import AccountUser
from exercises.models import Exercise

from .models import DayOfWeek, Routine, Progress


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
    def test_day_unicode(self):
        day = DayOfWeek.objects.create(day='monday')
        self.assertEqual(str(day), 'monday')

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
        add = self.client.post(reverse('dayofweek-list'), {'day': 'monday'})
        delete = self.client.delete(reverse('dayofweek-detail', args=(day.id, )))
        put = self.client.put(reverse('dayofweek-detail', args=(day.id, )), {'day': 'tuesday'})

        self.assertEqual(add.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(put.status_code, status.HTTP_403_FORBIDDEN)


class RoutineTest(BaseTestCase):
    def test_routine_unicode(self):
        routine = Routine.objects.create(user=self.test_user, name='mondays', )
        self.assertEqual(str(routine), 'mondays')

    def test_add_routine_non_admin(self):
        exercise = Exercise.objects.create(name='squats', description='squat', )
        self.create_non_admin_user()
        response = self.client.post(
            reverse('routine-list'),
            {'name': 'mondays', 'exercises': '%d' % exercise.id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Routine.objects.count(), 1)
        self.assertEqual(Routine.objects.get().name, 'mondays')

    def test_delete_routine_non_admin(self):
        self.create_non_admin_user()
        routine = Routine.objects.create(user=self.non_admin_user, name='mondays', )
        response = self.client.delete(reverse('routine-detail', args=(routine.id,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_routine_non_admin(self):
        exercise = Exercise.objects.create(name='squats', description='squat', )
        self.create_non_admin_user()
        routine = Routine.objects.create(user=self.non_admin_user, name='mondays', )
        response = self.client.put(
            reverse('routine-detail', args=(routine.id,)), {'name': 'tuesdays', 'exercises': '%d' % exercise.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Routine.objects.count(), 1)

    def test_permissions(self):
        """
        Ensure a user can't delete or update another user's routines
        """
        exercise = Exercise.objects.create(name='squats', description='squat', )
        routine = Routine.objects.create(user=self.test_user, name='mondays', )
        self.create_non_admin_user()

        delete = self.client.delete(reverse('routine-detail', args=(routine.id,)))
        put = self.client.put(
            reverse('routine-detail', args=(routine.id,)), {'name': 'tuesdays', 'exercises': '%d' % exercise.id}
        )

        self.assertEqual(delete.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(put.status_code, status.HTTP_404_NOT_FOUND)


class PublicRoutineTest(BaseTestCase):
    def test_get_public_routine_list(self):
        exercise = Exercise.objects.create(name='squats', description='squat', )
        self.client.post(
            reverse('routine-list'),
            {'name': 'mondays', 'exercises': '%d' % exercise.id, 'is_public': True}
        )
        self.client.post(
            reverse('routine-list'),
            {'name': 'mondays', 'exercises': '%d' % exercise.id, 'is_public': False}
        )
        response = self.client.get(reverse('public-routine-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Routine.objects.count(), 2)
        self.assertEqual(Routine.objects.filter(is_public=True).count(), 1)

    def test_get_public_routine_detail(self):
        exercise = Exercise.objects.create(name='squats', description='squat', )
        self.client.post(
            reverse('routine-list'),
            {'name': 'mondays', 'exercises': '%d' % exercise.id, 'is_public': True}
        )
        routine = Routine.objects.get()
        response = self.client.get(reverse('public-routine-detail', args=(routine.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permissions(self):
        exercise = Exercise.objects.create(name='squats', description='squat', )
        self.client.post(reverse('routine-list'), {'name': 'mondays', 'exercises': '%d' % exercise.id})
        routine = Routine.objects.get(name='mondays')

        post = self.client.post(reverse('public-routine-list'),  {'name': 'tuesdays', 'exercises': '%d' % exercise.id})
        delete = self.client.delete(reverse('public-routine-detail', args=(routine.id,)))
        put = self.client.put(
            reverse('public-routine-detail', args=(routine.id,)),
            {'name': 'wednesdays', 'exercises': '%d' % exercise.id}
        )

        self.assertEqual(post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ProgressTest(BaseTestCase):
    def test_progress_unicode(self):
        exercise = Exercise.objects.create(name='squats', description='squat', )
        progress = Progress.objects.create(user=self.test_user, exercise=exercise, date=datetime.date.today())
        self.assertEqual(str(progress), 'squats - %s' % (progress.date.strftime('%m/%d/%Y')))

    def test_add_progress_non_admin(self):
        exercise = Exercise.objects.create(name='squats', description='squat', )
        self.create_non_admin_user()
        response = self.client.post(
            reverse('progress-list'),
            {'user': self.non_admin_user.id, 'exercise': exercise.id, 'duration': '767', 'date': datetime.date.today()}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Progress.objects.count(), 1)
        self.assertEqual(Progress.objects.get().duration, 767)

    def test_delete_progress_non_admin(self):
        exercise = Exercise.objects.create(name='squats', description='squat', )

        self.create_non_admin_user()
        progress = Progress.objects.create(user=self.non_admin_user, exercise=exercise, date=datetime.date.today())
        response = self.client.delete(reverse('progress-detail', args=(progress.id,)))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Progress.objects.count(), 0)
        self.assertRaises(Progress.DoesNotExist, lambda: Progress.objects.get(id=progress.id))

    def test_delete_by_other_user(self):
        exercise = Exercise.objects.create(name='squats', description='squat', )
        progress = Progress.objects.create(user=self.test_user, exercise=exercise, date=datetime.date.today())

        self.create_non_admin_user()
        response = self.client.delete(reverse('progress-detail', args=(progress.id,)))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Progress.objects.count(), 1)
        self.assertTrue(Progress.objects.get(id=progress.id))

    def test_update_progress_non_admin(self):
        exercise = Exercise.objects.create(name='squats', description='squat', )

        self.create_non_admin_user()
        progress = Progress.objects.create(user=self.non_admin_user, exercise=exercise,
                                           date=datetime.date.today(), duration=767)
        put = self.client.put(
            reverse('progress-detail', args=(progress.id,)),
            {'duration': '940', 'date': datetime.date.today(), 'exercise': exercise.id}
        )
        put_duration = Progress.objects.get().duration

        patch = self.client.patch(reverse('progress-detail', args=(progress.id,)), {'duration': '214'})

        self.assertEqual(put.status_code, status.HTTP_200_OK)
        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.assertEqual(put_duration, 940)
        self.assertEqual(Progress.objects.get().duration, 214)
        self.assertEqual(Progress.objects.count(), 1)

    def test_permissions(self):
        exercise = Exercise.objects.create(name='squats', description='squat', )
        progress = Progress.objects.create(user=self.test_user, exercise=exercise,
                                           date=datetime.date.today(), duration=767)

        self.create_non_admin_user()

        delete = self.client.delete(reverse('progress-detail', args=(progress.id,)))
        put = self.client.put(
            reverse('progress-detail', args=(progress.id,)),
            {'duration': '940', 'date': datetime.date.today(), 'exercise': exercise.id}
        )
        patch = self.client.patch(reverse('progress-detail', args=(progress.id,)), {'duration': '214'})

        self.assertEqual(delete.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(put.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(patch.status_code, status.HTTP_404_NOT_FOUND)
