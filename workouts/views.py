from rest_framework import viewsets
from accounts.models import AccountUser
from .serializers import RoutineSerializer
from .models import Routine


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
