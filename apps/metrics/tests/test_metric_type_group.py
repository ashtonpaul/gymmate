from django.db import IntegrityError

from rest_framework import status
from rest_framework.reverse import reverse

from ...core.tests import MetricsTestCase

from ..models import Metric, MetricTypeGroup


class MetricGroupTypeTest(MetricsTestCase):
    def test_group_type_unicode(self):
        """
        Test unicode string representation for metric group
        """
        group = MetricTypeGroup.objects.create(name='height')
        self.assertEqual(str(group), 'height')

    def test_get_metric_group_type(self):
        """
        Ensure a metric group can be retrieved by an admin user
        """
        self.populate()
        self.authenticate(self.user_basic)
        group_list = self.client.get(reverse('metric-group-list'))
        detail = self.client.get(reverse('metric-group-detail', args=(self.group.id,)))

        self.assertEqual(group_list.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)

    def test_add_metric_group(self):
        """
        Ability to add a metric group type by an admin
        """
        self.authenticate(self.user_admin)
        response = self.client.post(reverse('metric-group-list'), {'name': 'weight'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MetricTypeGroup.objects.count(), 1)
        self.assertEqual(MetricTypeGroup.objects.get().name, 'weight')

    def test_unique_metric_group(self):
        """
        Ensure that metric type group names are unique
        """
        self.authenticate(self.user_admin)
        self.client.post(reverse('metric-group-list'), {'name': 'test_group'})
        self.assertRaises(IntegrityError, lambda: MetricTypeGroup.objects.create(name='test_group'))

    def test_metric_group_cascade(self):
        """
        If a type group is deleted all associated types and metrics should be deleted too
        """
        self.populate()
        self.client.delete(reverse('metric-group-detail', args=(self.group.id,)))
        self.assertRaises(Metric.DoesNotExist, lambda: Metric.objects.get(id=self.metric.id))

    def test_delete_metric(self):
        """
        Ensure an admin can delete a metric group
        """
        self.populate()
        response = self.client.delete(reverse('metric-group-detail', args=(self.group.id, )))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MetricTypeGroup.objects.count(), 0)
        self.assertRaises(
            MetricTypeGroup.DoesNotExist,
            lambda: MetricTypeGroup.objects.get(id=self.group.id)
        )

    def test_permissions(self):
        """
        Non-admin users do not have permission to alter metric type groups
        """
        self.populate()
        self.authenticate(self.user_basic)
        delete = self.client.delete(reverse('metric-group-detail', args=(self.group.id, )))
        put = self.client.put(reverse('metric-group-detail', args=(self.group.id, )), {'name': 'inches'})
        patch = self.client.patch(reverse('metric-group-detail', args=(self.group.id, )), {'name': 'inches'})

        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(put.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(patch.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_metric_group(self):
        """
        Ensure an admin can update a metric type group
        """
        self.populate()

        put = self.client.put(reverse('metric-group-detail', args=(self.group.id,)), {'name': 'weight'})
        updated_value = MetricTypeGroup.objects.get(id=self.group.id).name

        patch = self.client.patch(reverse('metric-group-detail', args=(self.group.id,)), {'name': 'height'})
        patched_value = MetricTypeGroup.objects.get(id=self.group.id).name

        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        self.assertEqual(patched_value, 'height')
        self.assertEqual(updated_value, 'weight')
        self.assertEqual(MetricTypeGroup.objects.count(), 1)
