import datetime

from rest_framework import status
from rest_framework.reverse import reverse

from ...core.tests import BaseTestCase
from ...exercises.models import Exercise

from ..models import Progress


class ProgressTest(BaseTestCase):
    def test_progress_unicode(self):
        """
        Test unicode string represenation of the progress entry
        """
        self.authenticate(self.user_admin)
        exercise = Exercise.objects.create(name='squats', description='squat', )
        progress = Progress.objects.create(user=self.user, exercise=exercise, date=datetime.date.today())
        self.assertEqual(str(progress), 'squats - %s' % (progress.date.strftime('%m/%d/%Y')))

    def test_get_progress(self):
        """
        Ensure that a user can retrieve their progress entries
        """
        self.authenticate(self.user_admin)
        exercise = Exercise.objects.create(name='squats', description='squat', )

        self.authenticate(self.user_basic)
        progress = Progress.objects.create(user=self.user, exercise=exercise, date=datetime.date.today())
        progress_list = self.client.get(reverse('progress-list'))
        detail = self.client.get(reverse('progress-detail', args=(progress.id,)))

        self.assertEqual(progress_list.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)

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
