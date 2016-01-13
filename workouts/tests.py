import datetime

from django.db import IntegrityError

from rest_framework import status
from rest_framework.reverse import reverse

from gymmate.tests import BaseTestCase
from exercises.models import Exercise

from .models import DayOfWeek, Routine, Progress


class DayOfWeekTest(BaseTestCase):
    def test_day_unicode(self):
        """
        Test unicode string represenation of the day of the week
        """
        day = DayOfWeek.objects.create(day='monday')
        self.assertEqual(str(day), 'monday')

    def test_add_day(self):
        """
        Add a day of the week by an admin user
        """
        self.authenticate(self.user_admin)
        response = self.client.post(reverse('dayofweek-list'), {'day': 'monday'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DayOfWeek.objects.count(), 1)
        self.assertEqual(DayOfWeek.objects.get().day, 'monday')

    def test_delete_day(self):
        """
        Delete a day of the week by an admin user
        """
        self.authenticate(self.user_admin)
        day = DayOfWeek.objects.create(day='monday')
        response = self.client.delete(reverse('dayofweek-detail', args=(day.id,)))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(DayOfWeek.objects.count(), 0)
        self.assertRaises(DayOfWeek.DoesNotExist, lambda: DayOfWeek.objects.get(id=day.id))

    def test_update_day(self):
        """
        Put and patch method on an object by admin user
        """
        day = DayOfWeek.objects.create(day='monday')
        self.authenticate(self.user_admin)
        self.client.put(reverse('dayofweek-detail', args=(day.id, )), {'day': 'tuesday'})
        day_updated = DayOfWeek.objects.get(id=day.id)

        self.assertEqual(day_updated.day, 'tuesday')
        self.assertEqual(DayOfWeek.objects.count(), 1)

    def test_unique(self):
        """
        Ensure that all values for day of week are unique
        """
        self.authenticate(self.user_admin)
        self.client.post(reverse('dayofweek-list'), {'day': 'monday'})
        self.assertRaises(IntegrityError, lambda: DayOfWeek.objects.create(day='monday'))

    def test_permissions(self):
        """
        Non-admin users are forbidden to perform non-safe methods on objects
        """
        day = DayOfWeek.objects.create(day='sunday')

        self.authenticate(self.user_basic)
        add = self.client.post(reverse('dayofweek-list'), {'day': 'monday'})
        delete = self.client.delete(reverse('dayofweek-detail', args=(day.id, )))
        put = self.client.put(reverse('dayofweek-detail', args=(day.id, )), {'day': 'tuesday'})
        patch = self.client.patch(reverse('dayofweek-detail', args=(day.id, )), {'day': 'tuesday'})

        self.assertEqual(add.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(put.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(patch.status_code, status.HTTP_403_FORBIDDEN)


class RoutineTest(BaseTestCase):
    def test_routine_unicode(self):
        """
        Test unicode string represenation of the routine
        """
        self.authenticate(self.user_admin)
        routine = Routine.objects.create(user=self.user, name='mondays', )
        self.assertEqual(str(routine), 'mondays')

    def test_add_routine_non_admin(self):
        """
        Ensure non-admin users can add exercise routines
        """
        exercise = Exercise.objects.create(name='squats', description='squat', )

        self.authenticate(self.user_basic)
        response = self.client.post(
            reverse('routine-list'),
            {'name': 'mondays', 'exercises': '%d' % exercise.id}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Routine.objects.count(), 1)
        self.assertEqual(Routine.objects.get().name, 'mondays')

    def test_delete_routine_non_admin(self):
        """
        Delete method test for exercise routines by non-admin users
        """
        self.authenticate(self.user_basic)
        routine = Routine.objects.create(user=self.user, name='mondays', )
        response = self.client.delete(reverse('routine-detail', args=(routine.id,)))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Routine.objects.count(), 0)

    def test_update_routine_non_admin(self):
        """
        Ensuer put/patch methods are available for non-admin users
        """
        exercise = Exercise.objects.create(name='squats', description='squat', )

        self.authenticate(self.user_basic)
        routine = Routine.objects.create(user=self.user, name='mondays', )

        patch = self.client.patch(reverse('routine-detail', args=(routine.id,)), {'name': 'tuesdays'})
        patched_routine = Routine.objects.get(id=routine.id)

        put = self.client.put(
            reverse('routine-detail', args=(routine.id,)), {'name': 'sundays', 'exercises': '%d' % exercise.id}
        )

        self.assertEqual(put.status_code, status.HTTP_200_OK)
        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.assertEqual(patched_routine.name, 'tuesdays')
        self.assertEqual(Routine.objects.get().name, 'sundays')
        self.assertEqual(Routine.objects.count(), 1)

    def test_permissions(self):
        """
        Ensure a user can't delete or update another user's routines
        """
        exercise = Exercise.objects.create(name='squats', description='squat', )

        self.authenticate(self.user_admin)
        routine = Routine.objects.create(user=self.user, name='mondays', )

        self.authenticate(self.user_basic)
        delete = self.client.delete(reverse('routine-detail', args=(routine.id,)))
        patch = self.client.patch(reverse('routine-detail', args=(routine.id,)), {'name': 'wednesdays'})
        put = self.client.put(
            reverse('routine-detail', args=(routine.id,)), {'name': 'tuesdays', 'exercises': '%d' % exercise.id}
        )

        self.assertEqual(delete.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(put.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(patch.status_code, status.HTTP_404_NOT_FOUND)


class PublicRoutineTest(BaseTestCase):
    def test_get_public_routine_list(self):
        """
        Ensure a list of all publicly shared routines is avilable to all users
        """
        self.authenticate(self.user_admin)
        Routine.objects.create(user=self.user, name='mondays', is_public=True)
        Routine.objects.create(user=self.user, name='tuesdays', is_public=False)
        Routine.objects.create(user=self.user, name='wednesdays', is_public=False)

        self.authenticate(self.user_basic)
        response = self.client.get(reverse('public-routine-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Routine.objects.count(), 3)
        self.assertEqual(Routine.objects.filter(is_public=True).count(), 1)

    def test_get_public_routine_detail(self):
        """
        Details of a publicly shared routine is available
        """
        self.authenticate(self.user_admin)
        routine = Routine.objects.create(user=self.user, name='mondays', is_public=True)
        response = self.client.get(reverse('public-routine-detail', args=(routine.id,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permissions(self):
        """
        Test Read-only permissions by other users
        """
        self.authenticate(self.user_admin)
        exercise = Exercise.objects.create(name='squats', description='squat', )
        routine = Routine.objects.create(user=self.user, name='mondays', is_public=True)

        post = self.client.post(reverse('public-routine-list'),  {'name': 'tuesdays', 'exercises': '%d' % exercise.id})
        delete = self.client.delete(reverse('public-routine-detail', args=(routine.id,)))
        patch = self.client.patch(
            reverse('public-routine-detail', args=(routine.id,)),
            {'name': 'wednesdays'}
        )
        put = self.client.put(
            reverse('public-routine-detail', args=(routine.id,)),
            {'name': 'thursdays', 'exercises': '%d' % exercise.id}
        )

        self.assertEqual(post.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(delete.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(put.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(patch.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class ProgressTest(BaseTestCase):
    def test_progress_unicode(self):
        """
        Test unicode string represenation of the progress entry
        """
        self.authenticate(self.user_admin)
        exercise = Exercise.objects.create(name='squats', description='squat', )
        progress = Progress.objects.create(user=self.user, exercise=exercise, date=datetime.date.today())
        self.assertEqual(str(progress), 'squats - %s' % (progress.date.strftime('%m/%d/%Y')))

    def test_add_progress_non_admin(self):
        """
        Add a progress entry by a non-admin user_admin
        """
        exercise = Exercise.objects.create(name='squats', description='squat', )

        self.authenticate(self.user_basic)
        response = self.client.post(
            reverse('progress-list'),
            {'user': self.user.id, 'exercise': exercise.id, 'duration': '767', 'date': datetime.date.today()}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Progress.objects.count(), 1)
        self.assertEqual(Progress.objects.get().duration, 767)

    def test_delete_progress_non_admin(self):
        """
        Ability to delete a progress entry by a non-admin user
        """
        exercise = Exercise.objects.create(name='squats', description='squat', )

        self.authenticate(self.user_basic)
        progress = Progress.objects.create(user=self.user, exercise=exercise, date=datetime.date.today())
        response = self.client.delete(reverse('progress-detail', args=(progress.id,)))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Progress.objects.count(), 0)
        self.assertRaises(Progress.DoesNotExist, lambda: Progress.objects.get(id=progress.id))

    def test_delete_by_other_user(self):
        """
        Ensure a non-admin user can't delete another user's progress entry
        """
        exercise = Exercise.objects.create(name='squats', description='squat', )

        self.authenticate(self.user_admin)
        progress = Progress.objects.create(user=self.user, exercise=exercise, date=datetime.date.today())

        self.authenticate(self.user_basic)
        response = self.client.delete(reverse('progress-detail', args=(progress.id,)))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Progress.objects.count(), 1)
        self.assertTrue(Progress.objects.get(id=progress.id))

    def test_update_progress_non_admin(self):
        """
        Ensure a non-admin user can patch and put on their progress entry
        """
        exercise = Exercise.objects.create(name='squats', description='squat', )

        self.authenticate(self.user_basic)
        progress = Progress.objects.create(user=self.user, exercise=exercise,
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

    def test_update_by_other_user(self):
        """
        Ensure a user can't delete another user's progress entry
        """
        self.authenticate(self.user_admin)
        exercise = Exercise.objects.create(name='squats', description='squat', )
        progress = Progress.objects.create(user=self.user, exercise=exercise, date=datetime.date.today(), duration=767)

        self.authenticate(self.user_basic)
        patch = self.client.patch(
            reverse('progress-detail', args=(progress.id,)),
            {'duration': '214'}
        )
        patched_progress = Progress.objects.get(id=progress.id)

        put = self.client.put(
            reverse('progress-detail', args=(progress.id,)),
            {'duration': '940', 'date': datetime.date.today(), 'exercise': exercise.id}
        )

        self.assertEqual(put.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(patch.status_code, status.HTTP_404_NOT_FOUND)
        self.assertNotEqual(patched_progress, 214)
        self.assertEqual(progress.duration, 767)
        self.assertEqual(Progress.objects.count(), 1)
