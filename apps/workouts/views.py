from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from ..core.permissions import IsAdminOrReadOnly
from ..core.loggers import LoggingMixin
from ..accounts.models import AccountUser

from .serializers import DayOfWeekSerializer, PublicRoutineSerializer, RoutineSerializer, ProgressSerializer
from .filters import DayOfWeekFilter, RoutineFilter, ProgressFilter
from .models import DayOfWeek, Routine, Progress


class WorkoutMixin(LoggingMixin, viewsets.ModelViewSet):
    """
    Abstract base class for workouts
    """
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    required_scopes = ['workouts']

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


class DayOfWeekViewSet(LoggingMixin, viewsets.ModelViewSet):
    """
    Generic class view to show days of week
    """
    permission_classes = [IsAdminOrReadOnly, TokenHasReadWriteScope]
    required_scopes = ['workouts']
    queryset = DayOfWeek.objects.all()
    serializer_class = DayOfWeekSerializer
    filter_class = DayOfWeekFilter


class PublicRoutineViewSet(LoggingMixin, viewsets.ModelViewSet):
    """
    List/Details of publically shared routines
    """
    permission_classes = [AllowAny, TokenHasReadWriteScope]
    required_scopes = ['workouts']
    queryset = Routine.objects.all()
    serializer_class = PublicRoutineSerializer
    filter_class = RoutineFilter
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        """
        Filter all routines that are marked for public viewing
        """
        return Routine.objects.filter(is_public=True)


class RoutineViewSet(WorkoutMixin):
    """
    List/Detail of a user's routine(s)
    """
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    filter_class = RoutineFilter

    def get_queryset(self):
        """
        Filter only current user's routine(s)
        """
        return Routine.objects.filter(user=self.request.user)


class ProrgressViewSet(WorkoutMixin):
    """
    List/Detail of a user's workout progression
    """
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    filter_class = ProgressFilter

    def get_queryset(self):
        """
        Filter only current user's progress logs
        """
        return Progress.objects.filter(user=self.request.user)
