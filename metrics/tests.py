import time

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
    def test_group_type_unicode(self):
        """
        Test unicode string representation for metric group
        """
        group = MetricTypeGroup.objects.create(name='height')
        self.assertEqual(str(group), 'height')

    def test_add_metric_group(self):
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
        self.client.delete(reverse('metric-group-detail', args=(self.last_created_group,)))

        self.assertRaises(Metric.DoesNotExist, lambda: Metric.objects.get(id=self.last_created_metric))

    def test_delete_metric(self):
        """
        Ensure an admin can delete a metric group
        """
        self.populate()
        response = self.client.delete(reverse('metric-group-detail', args=(self.last_created_group, )))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MetricTypeGroup.objects.count(), 0)
        self.assertRaises(
            MetricTypeGroup.DoesNotExist,
            lambda: MetricTypeGroup.objects.get(id=self.last_created_group)
        )

    def test_delete_non_admin(self):
        """
        Non-admin users do not have permission to delete metric type groups
        """
        self.populate()
        self.authenticate(self.user_basic)
        response = self.client.delete(reverse('metric-group-detail', args=(self.last_created_group, )))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MetricTypeTest(MetricsTestCase):
    def test_metric_unicode(self):
        """
        Test unicode string representation for metric type
        """
        group = MetricTypeGroup.objects.create(name='weight')
        metric_type = MetricType.objects.create(name='pounds', unit='lbs', group=group)
        self.assertEqual(str(metric_type), 'lbs')

    def test_add_metric_type(self):
        """
        Ability to add a metric type test by admin
        """
        self.authenticate(self.user_admin)
        group = MetricTypeGroup.objects.create(name='weight')
        response = self.client.post(
            reverse('metric-type-list'),
            {'name': 'pounds', 'unit': 'lbs', 'group': group.name}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MetricType.objects.count(), 1)
        self.assertEqual(MetricType.objects.get().name, 'pounds')

    def test_delete_metric(self):
        """
        Ensure an admin can delete a metric type
        """
        self.populate()
        response = self.client.delete(reverse('metric-type-detail', args=(self.last_created_type,)))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MetricType.objects.count(), 0)
        self.assertRaises(MetricType.DoesNotExist, lambda: MetricType.objects.get(id=self.last_created_type))

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
    def test_metric_unicode(self):
        """
        Test unicode string representation for metric entry
        """
        self.authenticate(self.user_basic)

        group = MetricTypeGroup.objects.create(name='height')
        type = MetricType.objects.create(group=group, name='inch', unit='in')
        metric = Metric.objects.create(user=self.user, metric_type=type, value='75')

        self.assertEqual(str(metric), '%s - 75in' % time.strftime('%m/%d/%Y'))

    def test_add_metric(self):
        """
        Add new metric
        """
        group = MetricTypeGroup.objects.create(name='test_add_metric')
        type = MetricType.objects.create(group=group, name='test', unit='test')

        self.authenticate(self.user_basic)
        response = self.client.post(reverse('metric-list'),
                                    {'user': self.user, 'metric_type': type.id, 'value': '75'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Metric.objects.count(), 1)
        self.assertEqual(Metric.objects.get().value, 75)

    def test_delete_metric(self):
        """
        Ensure a user can delete a metric entry
        """
        self.populate()
        response = self.client.delete(reverse('metric-detail', args=(self.last_created_metric,)))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Metric.objects.count(), 0)
        self.assertRaises(Metric.DoesNotExist, lambda: Metric.objects.get(id=self.last_created_metric))
