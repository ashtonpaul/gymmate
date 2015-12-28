from __future__ import unicode_literals

from django.db import models
from accounts.models import AccountUser


class MetricType(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=10)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return '%s' % (self.unit)


class Metric(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AccountUser, to_field='username')
    value = models.FloatField(blank=False)
    metric_type = models.ForeignKey(MetricType)

    class Meta:
        ordering = ('date',)
