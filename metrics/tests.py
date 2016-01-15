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
        self.group = MetricTypeGroup.objects.create(name='test_group')
        self.type = MetricType.objects.create(name='test_type', unit='test', group=self.group)
        self.metric = Metric.objects.create(user=self.user, metric_type=self.type, value='1')


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
        type_list = self.client.get(reverse('metric-type-list'))
        detail = self.client.get(reverse('metric-type-detail', args=(self.type.id,)))

        self.assertEqual(type_list.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)

    def test_add_metric_type(self):
        """
        Ability to add a metric type test by admin
        """
        self.populate()
        response = self.client.post(
            reverse('metric-type-list'),
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
        response = self.client.delete(reverse('metric-type-detail', args=(self.type.id,)))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MetricType.objects.count(), 0)
        self.assertRaises(MetricType.DoesNotExist, lambda: MetricType.objects.get(id=self.type.id))

    def test_metric_type_cascade(self):
        """
        If a type is deleted all associated metrics should be deleted too
        """
        self.populate()
        self.client.delete(reverse('metric-type-detail', args=(self.type.id,)))

        self.assertRaises(Metric.DoesNotExist, lambda: Metric.objects.get(id=self.metric.id))

    def test_permissions(self):
        """
        Non-admin users do not have permission to alter metric type
        """
        self.populate()
        self.authenticate(self.user_basic)
        delete = self.client.delete(reverse('metric-type-detail', args=(self.type.id, )))
        put = self.client.put(reverse('metric-type-detail', args=(self.type.id, )), {'name': 'pounds'})
        patch = self.client.patch(reverse('metric-type-detail', args=(self.type.id, )), {'name': 'pounds'})

        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(put.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(patch.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_metric_type(self):
        """
        Ensure an admin can update the metric types
        """
        self.populate()
        put = self.client.put(
            reverse('metric-type-detail', args=(self.type.id,)),
            {'name': 'pounds', 'unit': 'lbs', 'group': self.group.id}
        )
        updated_value = MetricType.objects.get(id=self.type.id).unit

        patch = self.client.patch(reverse('metric-type-detail', args=(self.type.id,)), {'unit': 'kg'})
        patched_value = MetricType.objects.get(id=self.type.id).unit

        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.assertEqual(put.status_code, status.HTTP_200_OK)
        self.assertEqual(patched_value, 'kg')
        self.assertEqual(updated_value, 'lbs')
        self.assertEqual(MetricType.objects.count(), 1)


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

    def test_get_metric(self):
        """
        Ensure a metric can be retrieved by a user
        """
        self.populate()
        metric_list = self.client.get(reverse('metric-list'))
        detail = self.client.get(reverse('metric-detail', args=(self.metric.id,)))

        self.assertEqual(metric_list.status_code, status.HTTP_200_OK)
        self.assertEqual(detail.status_code, status.HTTP_200_OK)

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
        response = self.client.delete(reverse('metric-detail', args=(self.metric.id,)))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Metric.objects.count(), 0)
        self.assertRaises(Metric.DoesNotExist, lambda: Metric.objects.get(id=self.metric.id))

    def test_update_metric(self):
        """
        Ensure a user can put/patch update on an existing metric entry
        """
        self.populate()
        patch = self.client.patch(reverse('metric-detail', args=(self.metric.id,)), {'value': '76'})
        patched_value = Metric.objects.get(id=self.metric.id).value

        put = self.client.put(
            reverse('metric-detail', args=(self.metric.id,)),
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

        get = self.client.get(reverse('metric-detail', args=(self.metric.id,)))
        delete = self.client.delete(reverse('metric-detail', args=(self.metric.id,)))
        put = self.client.put(reverse('metric-detail', args=(self.metric.id,)), {'value': '76'})
        patch = self.client.patch(reverse('metric-detail', args=(self.metric.id,)), {'value': '77'})

        self.assertEqual(get.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(delete.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(put.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(patch.status_code, status.HTTP_404_NOT_FOUND)
