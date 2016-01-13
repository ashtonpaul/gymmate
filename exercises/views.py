from rest_framework import viewsets

from gymmate.permissions import IsAdminOrReadOnly

from .models import Muscle, ExerciseCategory, Equipment, Exercise
from .serializers import MuscleSerializer, ExerciseCategorySerializer, EquipmentSerializer, ExerciseSerializer


class MuscleViewSet(viewsets.ModelViewSet):
    """
    List/Detail of all available muscles
    """
    permission_classes = (IsAdminOrReadOnly, )
    queryset = Muscle.objects.all()
    serializer_class = MuscleSerializer


class ExerciseCategoryViewSet(viewsets.ModelViewSet):
    """
    List/Detail of all exercises groups/categories
    """
    permission_classes = (IsAdminOrReadOnly, )
    queryset = ExerciseCategory.objects.all()
    serializer_class = ExerciseCategorySerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    List/Detail eqiupment in the gym
    """
    permission_classes = (IsAdminOrReadOnly, )
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
    """
    List/Detail all the exercises able to be performed
    """
    permission_classes = (IsAdminOrReadOnly, )
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
