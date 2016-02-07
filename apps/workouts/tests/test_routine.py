from rest_framework import status
from rest_framework.reverse import reverse

from ...core.tests import BaseTestCase
from ...exercises.models import Exercise

from ..models import Routine


class RoutineTest(BaseTestCase):
    def test_routine_unicode(self):
        """
        Test unicode string represenation of the routine
        """
        self.authenticate(self.user_admin)
        routine = Routine.objects.create(user=self.user, name='mondays', )
        self.assertEqual(str(routine), 'mondays')

    def test_get_routine(self):
        """
        Ensure a routine can be retrieved by an admin user
        """
        self.authenticate(self.user_basic)

        routine = Routine.objects.create(user=self.user, name='mondays', is_public=True)
        routine_list = self.client.get(reverse('public-routine-list'))
        detail = self.client.get(reverse('public-routine-detail', args=(routine.id,)))

        self.assertEqual(routine_list.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)

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
        self.assertRaises(Routine.DoesNotExist, lambda: Routine.objects.get(id=routine.id))

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
        public_routine_list = self.client.get(reverse('public-routine-list'))
        detail = self.client.get(reverse('public-routine-detail', args=(routine.id,)))

        self.assertEqual(public_routine_list.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)

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
