from rest_framework import viewsets
from .models import Metric, MetricType
from .serializers import MetricSerializer, MetricTypeSerializer


class MetricTypeViewSet(viewsets.ModelViewSet):
    queryset = MetricType.objects.all().order_by('name')
    serializer_class = MetricTypeSerializer


class MetricViewSet(viewsets.ModelViewSet):
    queryset = Metric.objects.all().order_by('date')
    serializer_class = MetricSerializer
