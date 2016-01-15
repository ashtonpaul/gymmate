from django.db import IntegrityError

from rest_framework import status
from rest_framework.reverse import reverse

from gymmate.tests import BaseTestCase
from workouts.models import DayOfWeek


class DayOfWeekTest(BaseTestCase):
    def test_day_unicode(self):
        """
        Test unicode string represenation of the day of the week
        """
        day = DayOfWeek.objects.create(day='monday')
        self.assertEqual(str(day), 'monday')

    def test_get_dayofweek(self):
        """
        Ensure that the days of the way are available
        """
        self.authenticate(self.user_admin)
        day = DayOfWeek.objects.create(day='monday')
        day_list = self.client.get(reverse('dayofweek-list'))
        detail = self.client.get(reverse('dayofweek-detail', args=(day.id,)))

        self.assertEqual(day_list.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)

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
        self.authenticate(self.user_admin)
        day = DayOfWeek.objects.create(day='monday')

        put = self.client.put(reverse('dayofweek-detail', args=(day.id, )), {'day': 'tuesday'})
        day_updated = DayOfWeek.objects.get(id=day.id)

        patch = self.client.patch(reverse('dayofweek-detail', args=(day.id, )), {'day': 'wednesday'})
        day_patched = DayOfWeek.objects.get(id=day.id)

        self.assertEqual(put.status_code, status.HTTP_200_OK)
        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.assertEqual(day_updated.day, 'tuesday')
        self.assertEqual(day_patched.day, 'wednesday')
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
