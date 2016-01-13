from django.db import IntegrityError

from rest_framework import status
from rest_framework.reverse import reverse

from gymmate.tests import BaseTestCase

from .models import Metric, MetricType, MetricTypeGroup


class MetricsTestCase(BaseTestCase):
    def populate(self):
        """
        Common base method for populating data for testing between models
        """
        self.authenticate(self.user_admin)
        self.group = self.client.post(reverse('metric-group-list'), {'name': 'test_group'})

        self.last_created_group = MetricTypeGroup.objects.latest('id').id

        self.client.post(reverse('metric-type-list'), {'group': 'test_group', 'name': 'test_type', 'unit': 'test'})
        self.last_created_type = MetricType.objects.latest('id').id

        self.client.post(reverse('metric-list'),
                         {'user': self.user, 'metric_type': self.last_created_type, 'value': '1'})
        self.last_created_metric = Metric.objects.latest('id').id


class MetricGroupTypeTest(MetricsTestCase):
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
        self.client.delete(reverse('metric-group-detail', args=(self.last_created_group,)))

        self.assertRaises(Metric.DoesNotExist, lambda: Metric.objects.get(id=self.last_created_metric))

    def test_delete_non_admin(self):
        """
        Non-admin users do not have permission to delete metric type groups
        """
        self.populate()
        self.authenticate(self.user_basic)
        response = self.client.delete(reverse('metric-group-detail', args=(self.last_created_group, )))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MetricTypeTest(MetricsTestCase):
    def test_metric_type_cascade(self):
        """
        If a type is deleted all associated metrics should be deleted too
        """
        self.populate()
        self.client.delete(reverse('metric-type-detail', args=(self.last_created_type,)))

        self.assertRaises(Metric.DoesNotExist, lambda: Metric.objects.get(id=self.last_created_metric))

    def test_delete_non_admin(self):
        """
        Non-admin users do not have permission to delete metric type
        """
        self.populate()
        self.authenticate(self.user_basic)
        response = self.client.delete(reverse('metric-type-detail', args=(self.last_created_type, )))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MetricTest(MetricsTestCase):
    def test_add_metric(self):
        """
        Add new metric
        """
        group = MetricTypeGroup.objects.create(name='test_add_metric')
        type = MetricType.objects.create(group=group, name='test', unit='test')

        self.authenticate(self.user_basic)
        response = self.client.post(reverse('metric-list'),
                                    {'user': self.user, 'metric_type': type.id, 'value': '1'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
