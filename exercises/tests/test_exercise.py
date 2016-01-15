from rest_framework import status
from rest_framework.reverse import reverse

from gymmate.tests import BaseTestCase
from exercises.models import Exercise


class ExerciseTest(BaseTestCase):
    def test_exercise_unicode(self):
        """
        Test unicode string represenation of an exercise
        """
        exercise = Exercise.objects.create(name='squats', description='squat')
        self.assertEqual(str(exercise), 'squats')

    def test_add_exercise(self):
        """
        Ensure an exercise object can be added
        """
        self.authenticate(self.user_admin)
        response = self.client.post(reverse('exercise-list'), {'name': 'squats', 'description': 'squat'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exercise.objects.count(), 1)
        self.assertEqual(Exercise.objects.get().name, 'squats')

    def test_update_exercise(self):
        """
        Ensure an equipment object can be updated by an admin user
        """
        self.authenticate(self.user_admin)
        exercise = Exercise.objects.create(name='squats', description='squat')
        patch = self.client.patch(reverse('exercise-detail', args=(exercise.id, )), {'name': 'leg squats'})
        exercise_patched = Exercise.objects.get(id=exercise.id)
        put = self.client.patch(reverse('exercise-detail', args=(exercise.id, )), {'name': 'bench press'})
        exercise_updated = Exercise.objects.get(id=exercise.id)

        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        self.assertEqual(exercise_updated.name, 'bench press')
        self.assertEqual(exercise_patched.name, 'leg squats')
        self.assertEqual(Exercise.objects.count(), 1)

    def test_delete_exercise(self):
        """
        Ensure an exercise object can be deleted
        """
        self.authenticate(self.user_admin)
        exercise = Exercise.objects.create(name='squats', description='squat')
        response = self.client.delete(reverse('exercise-detail', args=(exercise.id, )))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Exercise.objects.count(), 0)
        self.assertRaises(Exercise.DoesNotExist, lambda: Exercise.objects.get(name='squats'))

    def test_get_exercise(self):
        """
        Ensure an exercise object can be retrieved by a non admin user
        """
        Exercise.objects.create(name='squats', description='squat')

        self.authenticate(self.user_basic)
        exercise = Exercise.objects.get(name='squats')
        exercise_list = self.client.get(reverse('exercise-list'))
        detail = self.client.get(reverse('exercise-detail', args=(exercise.id, )))

        self.assertEqual(exercise_list.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)

    def test_non_admin_permissions(self):
        """
        Ensure that a non-admin user can not create, update or delete an exercise
        """
        exercise = Exercise.objects.create(name='squats', description='squat')

        self.authenticate(self.user_basic)
        post = self.client.post(reverse('exercise-list'), {'name': 'curl', 'description': 'bicep curl'})
        put = self.client.put(reverse('exercise-detail', args=(exercise.id,)), {'description': 'sqaut low'})
        delete = self.client.delete(reverse('exercise-detail', args=(exercise.id,)))

        self.assertEqual(post.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(put.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)
