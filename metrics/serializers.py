from rest_framework import serializers
from .models import Metric, MetricType, MetricTypeGroup


class MetricTypeGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MetricTypeGroup
        fields = ('id', 'name',)


class MetricTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MetricType
        fields = ('id', 'group', 'name', 'unit',)


class MetricSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Metric
        fields = ('date', 'user', 'value', 'metric_type', )
