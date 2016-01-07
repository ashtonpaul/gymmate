from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from accounts.models import AccountUser
from .models import Muscle, ExerciseCategory, Equipment


class BaseTestCase(APITestCase):
    def setUp(self):
        """
        Set up user for authentication to run tests
        """
        self.test_user = AccountUser.objects.create_user(username='test', password='test', is_active=True,
                                                         is_staff=True, is_superuser=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.test_user)


class MuscleTest(BaseTestCase):
    def test_add_muscle(self):
        response = self.client.post(reverse('muscle-list'), {'name': 'bicep'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_muscle(self):
        muscle = Muscle.objects.create(name='bicep')
        response = self.client.delete(reverse('muscle-detail', args=(muscle.id, )))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_muscle(self):
        muscle = Muscle.objects.create(name='bicep')
        self.client.put(reverse('muscle-detail', args=(muscle.id, )), {'name': 'tricep'})
        muscle_updated = Muscle.objects.get(id=muscle.id)
        self.assertEqual(muscle_updated.name, 'tricep')


class ExerciseCategoryTest(BaseTestCase):
    def test_add_exercise_category(self):
        response = self.client.post(reverse('exercise-category-list'), {'name': 'arms'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_exercise_category(self):
        exercise_category = ExerciseCategory.objects.create(name='arms')
        response = self.client.delete(reverse('exercise-category-detail', args=(exercise_category.id, )))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_exercise_category(self):
        exercise_category = ExerciseCategory.objects.create(name='arms')
        self.client.put(reverse('exercise-category-detail', args=(exercise_category.id, )), {'name': 'legs'})
        exercise_category_updated = ExerciseCategory.objects.get(id=exercise_category.id)
        self.assertEqual(exercise_category_updated.name, 'legs')


class EquipmentTest(BaseTestCase):
    def test_add_equipment(self):
        response = self.client.post(reverse('equipment-list'), {'name': 'barbell'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_equipment(self):
        equipment = Equipment.objects.create(name='barbell')
        response = self.client.delete(reverse('equipment-detail', args=(equipment.id, )))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_equipment(self):
        equipment = Equipment.objects.create(name='barbell')
        self.client.put(reverse('equipment-detail', args=(equipment.id, )), {'name': 'dumbbell'})
        equipment_updated = Equipment.objects.get(id=equipment.id)
        self.assertEqual(equipment_updated.name, 'dumbbell')
