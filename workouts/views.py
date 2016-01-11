from rest_framework import viewsets, status
from rest_framework.response import Response
from gymmate.permissions import IsAdminOrReadOnly
from accounts.models import AccountUser
from .serializers import DayOfWeekSerializer, RoutineSerializer, ProgressSerializer
from .models import DayOfWeek, Routine, Progress


class DayOfWeekViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    queryset = DayOfWeek.objects.all()
    serializer_class = DayOfWeekSerializer


class PublicRoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer
    http_method_names = ['get', 'head', 'options']

    def get_queryset(self):
        return Routine.objects.filter(is_public=True)


class RoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer

    def get_queryset(self):
        return Routine.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = AccountUser.objects.get(id=self.request.user.id)
        serializer.save(user=user)

    def perfom_update(self, serializer):
        user = AccountUser.objects.get(id=self.request.user.id)
        serializer.save(user=user)

    def update(self, request, *args, **kwargs):
        """
        return a 405 response if user tries to update a profile other than theirs
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if (instance.user.username == request.user.username):
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ProrgressViewSet(viewsets.ModelViewSet):
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer

    def get_queryset(self):
        return Progress.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = AccountUser.objects.get(id=self.request.user.id)
        serializer.save(user=user)

    def perfom_update(self, serializer):
        user = AccountUser.objects.get(id=self.request.user.id)
        serializer.save(user=user)
