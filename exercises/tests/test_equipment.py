from rest_framework import status
from rest_framework.reverse import reverse

from gymmate.tests import BaseTestCase
from ..models import Equipment


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
