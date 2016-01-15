from rest_framework import status
from rest_framework.reverse import reverse

from gymmate.tests import BaseTestCase

from .models import Muscle, ExerciseCategory, Equipment, Exercise


class MuscleTest(BaseTestCase):
    def test_muscle_unicode(self):
        """
        Test unicode string represenation of a muscle
        """
        muscle = Muscle.objects.create(name='biceps')
        self.assertEqual(str(muscle), 'biceps')

    def test_add_muscle(self):
        """
        Ensure a muscle object can be added by an admin user
        """
        self.authenticate(self.user_admin)
        response = self.client.post(reverse('muscle-list'), {'name': 'bicep'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Muscle.objects.count(), 1)
        self.assertEqual(Muscle.objects.get().name, 'bicep')

    def test_delete_muscle(self):
        """
        Ensure a muscle object can be deleted by an admin user
        """
        muscle = Muscle.objects.create(name='bicep')

        self.authenticate(self.user_admin)
        response = self.client.delete(reverse('muscle-detail', args=(muscle.id, )))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Muscle.objects.count(), 0)
        self.assertRaises(Muscle.DoesNotExist, lambda: Muscle.objects.get(name='bicep'))

    def test_update_muscle(self):
        """
        Ensure a muscle object can be updated by an admin user
        """
        muscle = Muscle.objects.create(name='bicep')

        self.authenticate(self.user_admin)
        put = self.client.put(reverse('muscle-detail', args=(muscle.id, )), {'name': 'tricep'})
        muscle_put = Muscle.objects.get(id=muscle.id)
        patch = self.client.patch(reverse('muscle-detail', args=(muscle.id, )), {'name': 'chest'})
        muscle_patch = Muscle.objects.get(id=muscle.id)

        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        self.assertEqual(muscle_put.name, 'tricep')
        self.assertEqual(muscle_patch.name, 'chest')
        self.assertEqual(Muscle.objects.count(), 1)

    def test_get_muscle(self):
        """
        Ensure a muscle object can be retrieved by a non admin user
        """
        self.authenticate(self.user_admin)
        self.client.post(reverse('muscle-list'), {'name': 'bicep'})

        self.authenticate(self.user_basic)
        muscle = Muscle.objects.get(name='bicep')
        muscle_list = self.client.get(reverse('muscle-list'))
        detail = self.client.get(reverse('muscle-detail', args=(muscle.id,)))

        self.assertEqual(muscle_list.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)

    def test_non_admin_permissions(self):
        """
        Ensure that a non-admin user can not create, update or delete an exercise
        """
        muscle = Muscle.objects.create(name='bicep')

        self.authenticate(self.user_basic)
        post = self.client.post(reverse('muscle-list'), {'name': 'tricep'})
        put = self.client.put(reverse('muscle-detail', args=(muscle.id,)), {'name': 'quad'})
        patch = self.client.patch(reverse('muscle-detail', args=(muscle.id,)), {'name': 'quad'})
        delete = self.client.delete(reverse('muscle-detail', args=(muscle.id,)))

        self.assertEqual(post.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(put.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(patch.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)


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
        response = self.client.post(reverse('exercise-category-list'), {'name': 'arms'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExerciseCategory.objects.count(), 1)
        self.assertEqual(ExerciseCategory.objects.get().name, 'arms')

    def test_delete_exercise_category(self):
        """
        Ensure an exercise category object can be deleted by an admin user
        """
        self.authenticate(self.user_admin)
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

        self.authenticate(self.user_admin)
        put = self.client.put(reverse('exercise-category-detail', args=(exercise_category.id, )), {'name': 'legs'})
        exercise_category_updated = ExerciseCategory.objects.get(id=exercise_category.id)

        patch = self.client.patch(
            reverse('exercise-category-detail', args=(exercise_category.id, )),
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
        self.client.post(reverse('exercise-category-list'), {'name': 'arms'})

        self.authenticate(self.user_basic)
        exercise_category = ExerciseCategory.objects.get(name='arms')
        detail = self.client.get(reverse('exercise-category-detail', args=(exercise_category.id, )))
        listing = self.client.get(reverse('exercise-category-list'))

        self.assertEqual(detail.status_code, status.HTTP_200_OK)
        self.assertEqual(listing.status_code, status.HTTP_200_OK)

    def test_non_admin_permissions(self):
        """
        Ensure that a non-admin user can not create, update or delete an exercise
        """
        exercise_category = ExerciseCategory.objects.create(name='arms')

        self.authenticate(self.user_basic)
        post = self.client.post(reverse('exercise-category-list'), {'name': 'legs'})
        put = self.client.put(reverse('exercise-category-detail', args=(exercise_category.id,)), {'name': 'torso'})
        delete = self.client.delete(reverse('exercise-category-detail', args=(exercise_category.id,)))

        self.assertEqual(post.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(put.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)


class EquipmentTest(BaseTestCase):
    def test_equipment_unicode(self):
        """
        Test unicode string represenation of equipment
        """
        equipment = Equipment.objects.create(name='dumbbell')
        self.assertEqual(str(equipment), 'dumbbell')

    def test_add_equipment(self):
        """
        Ensure an equipment object can be added by an admin user
        """
        self.authenticate(self.user_admin)
        response = self.client.post(reverse('equipment-list'), {'name': 'barbell'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Equipment.objects.count(), 1)
        self.assertEqual(Equipment.objects.get().name, 'barbell')

    def test_delete_equipment(self):
        """
        Ensure an equipment object can be deleted by an admin user
        """
        self.authenticate(self.user_admin)
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

        self.authenticate(self.user_admin)
        put = self.client.put(reverse('equipment-detail', args=(equipment.id, )), {'name': 'dumbbell'})
        equipment_updated = Equipment.objects.get(id=equipment.id)
        patch = self.client.patch(reverse('equipment-detail', args=(equipment.id, )), {'name': 'mat'})
        equipment_patched = Equipment.objects.get(id=equipment.id)

        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        self.assertEqual(equipment_patched.name, 'mat')
        self.assertEqual(equipment_updated.name, 'dumbbell')
        self.assertEqual(Equipment.objects.count(), 1)

    def test_get_equipment(self):
        """
        Ensure an equipment object can be retrieved by a non admin user
        """
        self.authenticate(self.user_admin)
        self.client.post(reverse('equipment-list'), {'name': 'barbell'})

        self.authenticate(self.user_basic)
        equipment = Equipment.objects.get(name='barbell')
        equipment_listing = self.client.get(reverse('equipment-list'))
        detail = self.client.get(reverse('equipment-detail', args=(equipment.id, )))

        self.assertEqual(equipment_listing.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)

    def test_non_admin_permissions(self):
        """
        Ensure that a non-admin user can not create, update or delete an exercise
        """
        equipment = Equipment.objects.create(name='barbell')

        self.authenticate(self.user_basic)
        post = self.client.post(reverse('equipment-list'), {'name': 'dumbbell'})
        put = self.client.put(reverse('equipment-detail', args=(equipment.id,)), {'name': 'ball'})
        delete = self.client.delete(reverse('equipment-detail', args=(equipment.id,)))

        self.assertEqual(post.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(put.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)


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
