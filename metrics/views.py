from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from gymmate.permissions import IsAdminOrReadOnly
from accounts.models import AccountUser

from .models import Metric, MetricType, MetricTypeGroup
from .serializers import MetricSerializer, MetricTypeSerializer, MetricTypeGroupSerializer


class MetricTypeGroupViewSet(viewsets.ModelViewSet):
    """
    List/Detail for Measurement group types
    """
    permission_classes = (IsAdminOrReadOnly, )
    queryset = MetricTypeGroup.objects.all().order_by('name')
    serializer_class = MetricTypeGroupSerializer


class MetricTypeViewSet(viewsets.ModelViewSet):
    """
    List/Detail for Metric Types
    """
    permission_classes = (IsAdminOrReadOnly, )
    queryset = MetricType.objects.all().order_by('name')
    serializer_class = MetricTypeSerializer


class MetricViewSet(viewsets.ModelViewSet):
    """
    User body measurment viewset
    """
    permission_classes = (IsAuthenticated, )
    queryset = Metric.objects.all().order_by('date')
    serializer_class = MetricSerializer

    def get_queryset(self):
        """
        Filter only current user's metrics
        """
        return Metric.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically assign requesting user to models user field
        """
        user = AccountUser.objects.get(id=self.request.user.id)
        serializer.save(user=user)
