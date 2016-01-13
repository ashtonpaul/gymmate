from rest_framework import viewsets

from gymmate.permissions import IsAdminOrReadOnly
from accounts.models import AccountUser

from .serializers import DayOfWeekSerializer, PublicRoutineSerializer, RoutineSerializer, ProgressSerializer
from .models import DayOfWeek, Routine, Progress


class DayOfWeekViewSet(viewsets.ModelViewSet):
    """
    Generic class view to show days of week
    """
    permission_classes = (IsAdminOrReadOnly,)
    queryset = DayOfWeek.objects.all()
    serializer_class = DayOfWeekSerializer


class PublicRoutineViewSet(viewsets.ModelViewSet):
    """
    List/Details of publically shared routines
    """
    queryset = Routine.objects.all()
    serializer_class = PublicRoutineSerializer
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        """
        Filter all routines that are marked for public viewing
        """
        return Routine.objects.filter(is_public=True)


class RoutineViewSet(viewsets.ModelViewSet):
    """
    List/Detail of a user's routine(s)
    """
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer

    def get_queryset(self):
        """
        Filter only current user's routine(s)
        """
        return Routine.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically assign requesting user to models user field
        """
        user = AccountUser.objects.get(id=self.request.user.id)
        serializer.save(user=user)

    def perform_update(self, serializer):
        """
        Automatically assign requesting user to models user field
        """
        user = AccountUser.objects.get(id=self.request.user.id)
        serializer.save(user=user)


class ProrgressViewSet(viewsets.ModelViewSet):
    """
    List/Detail of a user's workout progression
    """
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer

    def get_queryset(self):
        """
        Filter only current user's progress logs
        """
        return Progress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically assign requesting user to models user field
        """
        user = AccountUser.objects.get(id=self.request.user.id)
        serializer.save(user=user)

    def perform_update(self, serializer):
        """
        Automatically assign requesting user to models user field
        """
        user = AccountUser.objects.get(id=self.request.user.id)
        serializer.save(user=user)
