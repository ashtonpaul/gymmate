from rest_framework import viewsets
from gymmate.permissions import IsAdminOrReadOnly
from .models import Metric, MetricType, MetricTypeGroup
from .serializers import MetricSerializer, MetricTypeSerializer, MetricTypeGroupSerializer
from accounts.models import AccountUser


class MetricTypeGroupViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly, )
    queryset = MetricTypeGroup.objects.all().order_by('name')
    serializer_class = MetricTypeGroupSerializer


class MetricTypeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly, )
    queryset = MetricType.objects.all().order_by('name')
    serializer_class = MetricTypeSerializer


class MetricViewSet(viewsets.ModelViewSet):
    queryset = Metric.objects.all().order_by('date')
    serializer_class = MetricSerializer

    def get_queryset(self):
        return Metric.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = AccountUser.objects.get(id=self.request.user.id)
        serializer.save(user=user)

    def perfom_update(self, serializer):
        user = AccountUser.objects.get(id=self.request.user.id)
        serializer.save(user=user)
