from datetime import datetime

from rest_framework import status
from rest_framework.reverse import reverse

from ...core.tests import MetricsTestCase

from ..models import Metric, MetricType, MetricTypeGroup


class MetricTest(MetricsTestCase):
    def test_metric_unicode(self):
        """
        Test unicode string representation for metric entry
        """
        self.authenticate(self.user_basic)

        group = MetricTypeGroup.objects.create(name='height')
        type = MetricType.objects.create(group=group, name='inch', unit='in')
        metric = Metric.objects.create(user=self.user, metric_type=type, value='75')
        now = datetime.utcnow()

        self.assertEqual(str(metric), '%s - 75in' % now.strftime('%m/%d/%Y'))

    def test_get_metric(self):
        """
        Ensure a metric can be retrieved by a user
        """
        self.populate()
        metric_list = self.client.get(reverse('v1:metric-list'))
        detail = self.client.get(reverse('v1:metric-detail', args=(self.metric.id,)))

        self.assertEqual(metric_list.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)

    def test_add_metric(self):
        """
        Add new metric
        """
        group = MetricTypeGroup.objects.create(name='test_add_metric')
        type = MetricType.objects.create(group=group, name='test', unit='test')

        self.authenticate(self.user_basic)
        response = self.client.post(reverse('v1:metric-list'),
                                    {'user': self.user, 'metric_type': type.id, 'value': '75'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Metric.objects.count(), 1)
        self.assertEqual(Metric.objects.get().value, 75)

    def test_delete_metric(self):
        """
        Ensure a user can delete a metric entry
        """
        self.populate()
        response = self.client.delete(reverse('v1:metric-detail', args=(self.metric.id,)))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Metric.objects.count(), 0)
        self.assertRaises(Metric.DoesNotExist, lambda: Metric.objects.get(id=self.metric.id))

    def test_update_metric(self):
        """
        Ensure a user can put/patch update on an existing metric entry
        """
        self.populate()
        patch = self.client.patch(reverse('v1:metric-detail', args=(self.metric.id,)), {'value': '76'})
        patched_value = Metric.objects.get(id=self.metric.id).value

        put = self.client.put(
            reverse('v1:metric-detail', args=(self.metric.id,)),
            {'value': '77', 'metric_type': self.type.id}
        )
        updated_value = Metric.objects.get(id=self.metric.id).value

        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        self.assertEqual(patched_value, 76)
        self.assertEqual(updated_value, 77)
        self.assertEqual(Metric.objects.count(), 1)

    def test_permissions(self):
        """
        Ensure a user cannot access/alter another user's metric entries
        """
        self.populate()
        self.authenticate(self.user_basic)

        get = self.client.get(reverse('v1:metric-detail', args=(self.metric.id,)))
        delete = self.client.delete(reverse('v1:metric-detail', args=(self.metric.id,)))
        put = self.client.put(reverse('v1:metric-detail', args=(self.metric.id,)), {'value': '76'})
        patch = self.client.patch(reverse('v1:metric-detail', args=(self.metric.id,)), {'value': '77'})

        self.assertEqual(get.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(delete.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(put.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(patch.status_code, status.HTTP_404_NOT_FOUND)
