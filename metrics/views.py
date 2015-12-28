from rest_framework import viewsets
from .models import Metric, MetricType, MetricTypeGroup
from .serializers import MetricSerializer, MetricTypeSerializer, MetricTypeGroupSerializer


class MetricTypeGroupViewSet(viewsets.ModelViewSet):
    queryset = MetricTypeGroup.objects.all().order_by('name')
    serializer_class = MetricTypeGroupSerializer


class MetricTypeViewSet(viewsets.ModelViewSet):
    queryset = MetricType.objects.all().order_by('name')
    serializer_class = MetricTypeSerializer


class MetricViewSet(viewsets.ModelViewSet):
    queryset = Metric.objects.all().order_by('date')
    serializer_class = MetricSerializer
