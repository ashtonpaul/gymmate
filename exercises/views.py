from rest_framework import viewsets
from gymmate.permissions import IsAdminOrReadOnly
from .models import Muscle, ExerciseCategory, Equipment, Exercise
from .serializers import MuscleSerializer, ExerciseCategorySerializer, EquipmentSerializer, ExerciseSerializer


class MuscleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly, )
    queryset = Muscle.objects.all()
    serializer_class = MuscleSerializer


class ExerciseCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly, )
    queryset = ExerciseCategory.objects.all()
    serializer_class = ExerciseCategorySerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly, )
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly, )
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
