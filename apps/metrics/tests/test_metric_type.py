from rest_framework import status
from rest_framework.reverse import reverse

from ...core.tests import MetricsTestCase

from ..models import Metric, MetricType, MetricTypeGroup


class MetricTypeTest(MetricsTestCase):
    def test_metric_unicode(self):
        """
        Test unicode string representation for metric type
        """
        group = MetricTypeGroup.objects.create(name='weight')
        metric_type = MetricType.objects.create(name='pounds', unit='lbs', group=group)
        self.assertEqual(str(metric_type), 'lbs')

    def test_get_metric_type(self):
        """
        Ensure a metric type can be retrieved by an admin user
        """
        self.populate()
        self.authenticate(self.user_basic)
        type_list = self.client.get(reverse('v1:metric-type-list'))
        detail = self.client.get(reverse('v1:metric-type-detail', args=(self.type.id,)))

        self.assertEqual(type_list.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)

    def test_add_metric_type(self):
        """
        Ability to add a metric type test by admin
        """
        self.populate()
        response = self.client.post(
            reverse('v1:metric-type-list'),
            {'group': self.group.id, 'name': 'pounds', 'unit': 'lbs'}
        )
        type = MetricType.objects.get(unit='lbs')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MetricType.objects.count(), 2)
        self.assertEqual(type.name, 'pounds')

    def test_delete_metric_type(self):
        """
        Ensure an admin can delete a metric type
        """
        self.populate()
        response = self.client.delete(reverse('v1:metric-type-detail', args=(self.type.id,)))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MetricType.objects.count(), 0)
        self.assertRaises(MetricType.DoesNotExist, lambda: MetricType.objects.get(id=self.type.id))

    def test_metric_type_cascade(self):
        """
        If a type is deleted all associated metrics should be deleted too
        """
        self.populate()
        self.client.delete(reverse('v1:metric-type-detail', args=(self.type.id,)))

        self.assertRaises(Metric.DoesNotExist, lambda: Metric.objects.get(id=self.metric.id))

    def test_permissions(self):
        """
        Non-admin users do not have permission to alter metric type
        """
        self.populate()
        self.authenticate(self.user_basic)
        delete = self.client.delete(reverse('v1:metric-type-detail', args=(self.type.id, )))
        put = self.client.put(reverse('v1:metric-type-detail', args=(self.type.id, )), {'name': 'pounds'})
        patch = self.client.patch(reverse('v1:metric-type-detail', args=(self.type.id, )), {'name': 'pounds'})

        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(put.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(patch.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_metric_type(self):
        """
        Ensure an admin can update the metric types
        """
        self.populate()
        put = self.client.put(
            reverse('v1:metric-type-detail', args=(self.type.id,)),
            {'name': 'pounds', 'unit': 'lbs', 'group': self.group.id}
        )
        updated_value = MetricType.objects.get(id=self.type.id).unit

        patch = self.client.patch(reverse('v1:metric-type-detail', args=(self.type.id,)), {'unit': 'kg'})
        patched_value = MetricType.objects.get(id=self.type.id).unit

        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        self.assertEqual(patched_value, 'kg')
        self.assertEqual(updated_value, 'lbs')
        self.assertEqual(MetricType.objects.count(), 1)
