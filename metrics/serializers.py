from rest_framework import serializers
from .models import Metric, MetricType


class MetricTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MetricType
        fields = ('id', 'name', 'unit',)


class MetricSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Metric
        fields = ('date', 'user', 'value', 'metric_type', )
