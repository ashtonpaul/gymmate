from django.db import models

from accounts.models import AccountUser


class MetricTypeGroup(models.Model):
    """
    Parent group for each metric type
    """
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return '%s' % (self.name)


class MetricType(models.Model):
    """
    Type of metric to be measured
    """
    group = models.ForeignKey(MetricTypeGroup)
    name = models.CharField(max_length=50)
    unit = models.CharField(max_length=10)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return '%s' % (self.unit, )


class Metric(models.Model):
    """
    Metric model to store user biometric measurements
    """
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(AccountUser, to_field='username')
    value = models.FloatField(blank=False)
    metric_type = models.ForeignKey(MetricType)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return ('%s - %s%s' % (self.date.strftime('%m/%d/%Y'), str(self.value), self.metric_type))
