from rest_framework import serializers

from .models import Metric, MetricType, MetricTypeGroup


class MetricTypeGroupSerializer(serializers.HyperlinkedModelSerializer):
    """
    Measurement group type serializer
    """
    class Meta:
        model = MetricTypeGroup
        fields = ('id', 'name',)


class MetricTypeSerializer(serializers.HyperlinkedModelSerializer):
    """
    Metric type serializer
    """
    class Meta:
        model = MetricType
        fields = ('id', 'group', 'name', 'unit',)


class MetricSerializer(serializers.ModelSerializer):
    """
    User measurement serializer
    """
    class Meta:
        model = Metric
        exclude = ('user',)
