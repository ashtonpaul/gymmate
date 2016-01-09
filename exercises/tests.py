from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from accounts.models import AccountUser
from .models import Muscle, ExerciseCategory, Equipment, Exercise


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


class MuscleTest(BaseTestCase):
    def test_add_muscle(self):
        """
        Ensure a muscle object can be added by an admin user
        """
        response = self.client.post(reverse('muscle-list'), {'name': 'bicep'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Muscle.objects.count(), 1)
        self.assertEqual(Muscle.objects.get().name, 'bicep')

    def test_delete_muscle(self):
        """
        Ensure a muscle object can be deleted by an admin user
        """
        muscle = Muscle.objects.create(name='bicep')
        response = self.client.delete(reverse('muscle-detail', args=(muscle.id, )))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Muscle.objects.count(), 0)
        self.assertRaises(Muscle.DoesNotExist, lambda: Muscle.objects.get(name='bicep'))

    def test_update_muscle(self):
        """
        Ensure a muscle object can be updated by and admin user
        """
        muscle = Muscle.objects.create(name='bicep')
        self.client.put(reverse('muscle-detail', args=(muscle.id, )), {'name': 'tricep'})
        muscle_updated = Muscle.objects.get(id=muscle.id)
        self.assertEqual(muscle_updated.name, 'tricep')

    def test_get_muscle(self):
        """
        Ensure a muscle object can be retrieved by a non admin user
        """
        self.client.post(reverse('muscle-list'), {'name': 'bicep'})
        self.create_non_admin_user()
        muscle = Muscle.objects.get(name='bicep')
        response = self.client.get(reverse('muscle-detail', args=(muscle.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_admin_permissions(self):
        """
        Ensure that a non-admin user can not create, update or delete an exercise
        """
        muscle = Muscle.objects.create(name='bicep')

        self.create_non_admin_user()
        post = self.client.post(reverse('muscle-list'), {'name': 'tricep'})
        put = self.client.put(reverse('muscle-detail', args=(muscle.id,)), {'name': 'quad'})
        delete = self.client.delete(reverse('muscle-detail', args=(muscle.id,)))

        self.assertEqual(post.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(put.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)


class ExerciseCategoryTest(BaseTestCase):
    def test_add_exercise_category(self):
        """
        Ensure an exercise category object can be added by an admin user
        """
        response = self.client.post(reverse('exercise-category-list'), {'name': 'arms'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExerciseCategory.objects.count(), 1)
        self.assertEqual(ExerciseCategory.objects.get().name, 'arms')

    def test_delete_exercise_category(self):
        """
        Ensure an exercise category object can be deleted by an admin user
        """
        exercise_category = ExerciseCategory.objects.create(name='arms')
        response = self.client.delete(reverse('exercise-category-detail', args=(exercise_category.id, )))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ExerciseCategory.objects.count(), 0)
        self.assertRaises(ExerciseCategory.DoesNotExist, lambda: ExerciseCategory.objects.get(name='arms'))

    def test_update_exercise_category(self):
        """
        Ensure an exercise category object can be deleted by an admin user
        """
        exercise_category = ExerciseCategory.objects.create(name='arms')
        self.client.put(reverse('exercise-category-detail', args=(exercise_category.id, )), {'name': 'legs'})
        exercise_category_updated = ExerciseCategory.objects.get(id=exercise_category.id)
        self.assertEqual(exercise_category_updated.name, 'legs')

    def test_get_exercise_category(self):
        """
        Ensure an exercise category object can be retrieved by a non admin user
        """
        self.client.post(reverse('exercise-category-list'), {'name': 'arms'})
        self.create_non_admin_user()
        exercise_category = ExerciseCategory.objects.get(name='arms')
        response = self.client.get(reverse('exercise-category-detail', args=(exercise_category.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_admin_permissions(self):
        """
        Ensure that a non-admin user can not create, update or delete an exercise
        """
        exercise_category = ExerciseCategory.objects.create(name='arms')

        self.create_non_admin_user()
        post = self.client.post(reverse('exercise-category-list'), {'name': 'legs'})
        put = self.client.put(reverse('exercise-category-detail', args=(exercise_category.id,)), {'name': 'torso'})
        delete = self.client.delete(reverse('exercise-category-detail', args=(exercise_category.id,)))

        self.assertEqual(post.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(put.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)


class EquipmentTest(BaseTestCase):
    def test_add_equipment(self):
        """
        Ensure an equipment object can be added by an admin user
        """
        response = self.client.post(reverse('equipment-list'), {'name': 'barbell'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Equipment.objects.count(), 1)
        self.assertEqual(Equipment.objects.get().name, 'barbell')

    def test_delete_equipment(self):
        """
        Ensure an equipment object can be deleted by an admin user
        """
        equipment = Equipment.objects.create(name='barbell')
        response = self.client.delete(reverse('equipment-detail', args=(equipment.id, )))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Equipment.objects.count(), 0)
        self.assertRaises(Equipment.DoesNotExist, lambda: Equipment.objects.get(name='barbell'))

    def test_update_equipment(self):
        """
        Ensure an equipment object can be updated by an admin user
        """
        equipment = Equipment.objects.create(name='barbell')
        self.client.put(reverse('equipment-detail', args=(equipment.id, )), {'name': 'dumbbell'})
        equipment_updated = Equipment.objects.get(id=equipment.id)
        self.assertEqual(equipment_updated.name, 'dumbbell')

    def test_get_equipment(self):
        """
        Ensure an equipment object can be retrieved by a non admin user
        """
        self.client.post(reverse('equipment-list'), {'name': 'barbell'})
        self.create_non_admin_user()
        equipment = Equipment.objects.get(name='barbell')
        response = self.client.get(reverse('equipment-detail', args=(equipment.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_admin_permissions(self):
        """
        Ensure that a non-admin user can not create, update or delete an exercise
        """
        equipment = Equipment.objects.create(name='barbell')

        self.create_non_admin_user()
        post = self.client.post(reverse('equipment-list'), {'name': 'dumbbell'})
        put = self.client.put(reverse('equipment-detail', args=(equipment.id,)), {'name': 'ball'})
        delete = self.client.delete(reverse('equipment-detail', args=(equipment.id,)))

        self.assertEqual(post.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(put.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)


class ExerciseTest(BaseTestCase):
    def test_add_exercise(self):
        """
        Ensure an exercise object can be added
        """
        response = self.client.post(reverse('exercise-list'), {'name': 'squats', 'description': 'squat'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exercise.objects.count(), 1)
        self.assertEqual(Exercise.objects.get().name, 'squats')

    def test_update_exercise(self):
        """
        Ensure an equipment object can be updated by an admin user
        """
        exercise = Exercise.objects.create(name='squats', description='squat')
        self.client.patch(reverse('exercise-detail', args=(exercise.id, )), {'name': 'leg squats'})
        exercise_updated = Exercise.objects.get(id=exercise.id)
        self.assertEqual(exercise_updated.name, 'leg squats')

    def test_delete_exercise(self):
        """
        Ensure an exercise object can be deleted
        """
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
        self.create_non_admin_user()

        exercise = Exercise.objects.get(name='squats')
        response = self.client.get(reverse('exercise-detail', args=(exercise.id, )))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_admin_permissions(self):
        """
        Ensure that a non-admin user can not create, update or delete an exercise
        """
        exercise = Exercise.objects.create(name='squats', description='squat')

        self.create_non_admin_user()
        post = self.client.post(reverse('exercise-list'), {'name': 'curl', 'description': 'bicep curl'})
        put = self.client.put(reverse('exercise-detail', args=(exercise.id,)), {'description': 'sqaut low'})
        delete = self.client.delete(reverse('exercise-detail', args=(exercise.id,)))

        self.assertEqual(post.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(put.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)
