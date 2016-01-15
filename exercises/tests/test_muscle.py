from rest_framework import status
from rest_framework.reverse import reverse

from gymmate.tests import BaseTestCase
from exercises.models import Muscle


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
