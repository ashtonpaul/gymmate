from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Metric, MetricType, MetricTypeGroup
from .serializers import MetricSerializer, MetricTypeSerializer, MetricTypeGroupSerializer


class MetricTypeGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser, )
    queryset = MetricTypeGroup.objects.all().order_by('name')
    serializer_class = MetricTypeGroupSerializer


class MetricTypeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminUser, )
    queryset = MetricType.objects.all().order_by('name')
    serializer_class = MetricTypeSerializer


class MetricViewSet(viewsets.ModelViewSet):
    queryset = Metric.objects.all().order_by('date')
    serializer_class = MetricSerializer

    def get_queryset(self):
        user = self.request.user
        return Metric.objects.filter(user=user)
