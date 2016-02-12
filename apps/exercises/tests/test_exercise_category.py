from rest_framework import status
from rest_framework.reverse import reverse

from ...core.tests import BaseTestCase

from ..models import ExerciseCategory


class ExerciseCategoryTest(BaseTestCase):
    def test_exercise_category_unicode(self):
        """
        Test unicode string represenation of an exercise category
        """
        exercise_category = ExerciseCategory.objects.create(name='arms')
        self.assertEqual(str(exercise_category), 'arms')

    def test_add_exercise_category(self):
        """
        Ensure an exercise category object can be added by an admin user
        """
        self.authenticate(self.user_admin)
        response = self.client.post(reverse('v1:exercise-category-list'), {'name': 'arms'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExerciseCategory.objects.count(), 1)
        self.assertEqual(ExerciseCategory.objects.get().name, 'arms')

    def test_delete_exercise_category(self):
        """
        Ensure an exercise category object can be deleted by an admin user
        """
        self.authenticate(self.user_admin)
        exercise_category = ExerciseCategory.objects.create(name='arms')
        response = self.client.delete(reverse('v1:exercise-category-detail', args=(exercise_category.id, )))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ExerciseCategory.objects.count(), 0)
        self.assertRaises(ExerciseCategory.DoesNotExist, lambda: ExerciseCategory.objects.get(name='arms'))

    def test_update_exercise_category(self):
        """
        Ensure an exercise category object can be deleted by an admin user
        """
        exercise_category = ExerciseCategory.objects.create(name='arms')

        self.authenticate(self.user_admin)
        put = self.client.put(reverse('v1:exercise-category-detail', args=(exercise_category.id, )), {'name': 'legs'})
        exercise_category_updated = ExerciseCategory.objects.get(id=exercise_category.id)

        patch = self.client.patch(
            reverse('v1:exercise-category-detail', args=(exercise_category.id, )),
            {'name': 'chest'}
        )
        exercise_category_patched = ExerciseCategory.objects.get(id=exercise_category.id)

        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        self.assertEqual(exercise_category_updated.name, 'legs')
        self.assertEqual(exercise_category_patched.name, 'chest')
        self.assertEqual(ExerciseCategory.objects.count(), 1)

    def test_get_exercise_category(self):
        """
        Ensure an exercise category object can be retrieved by a non admin user
        """
        self.authenticate(self.user_admin)
        self.client.post(reverse('v1:exercise-category-list'), {'name': 'arms'})

        self.authenticate(self.user_basic)
        exercise_category = ExerciseCategory.objects.get(name='arms')
        detail = self.client.get(reverse('v1:exercise-category-detail', args=(exercise_category.id, )))
        listing = self.client.get(reverse('v1:exercise-category-list'))

        self.assertEqual(detail.status_code, status.HTTP_200_OK)
        self.assertEqual(listing.status_code, status.HTTP_200_OK)

    def test_non_admin_permissions(self):
        """
        Ensure that a non-admin user can not create, update or delete an exercise
        """
        exercise_category = ExerciseCategory.objects.create(name='arms')

        self.authenticate(self.user_basic)
        post = self.client.post(reverse('v1:exercise-category-list'), {'name': 'legs'})
        put = self.client.put(reverse('v1:exercise-category-detail', args=(exercise_category.id,)), {'name': 'torso'})
        delete = self.client.delete(reverse('v1:exercise-category-detail', args=(exercise_category.id,)))

        self.assertEqual(post.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(put.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)
