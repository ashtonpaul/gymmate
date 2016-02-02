from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope

from rest_framework import viewsets

from gymmate.permissions import IsAdminOrReadOnly

from .models import Muscle, ExerciseCategory, Equipment, Exercise
from .filters import MuscleFilter, ExerciseCategoryFilter, EquipmentFilter, ExerciseFilter
from .serializers import MuscleSerializer, ExerciseCategorySerializer, EquipmentSerializer, ExerciseSerializer


class MuscleViewSet(viewsets.ModelViewSet):
    """
    List/Detail of all available muscles
    """
    permission_classes = [IsAdminOrReadOnly, TokenHasReadWriteScope]
    required_scopes = ['exercises']
    queryset = Muscle.objects.all()
    serializer_class = MuscleSerializer
    filter_class = MuscleFilter


class ExerciseCategoryViewSet(viewsets.ModelViewSet):
    """
    List/Detail of all exercises groups/categories
    """
    permission_classes = [IsAdminOrReadOnly, TokenHasReadWriteScope]
    required_scopes = ['exercises']
    queryset = ExerciseCategory.objects.all()
    serializer_class = ExerciseCategorySerializer
    filter_class = ExerciseCategoryFilter


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    List/Detail eqiupment in the gym
    """
    permission_classes = [IsAdminOrReadOnly, TokenHasReadWriteScope]
    required_scopes = ['exercises']
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filter_class = EquipmentFilter


class ExerciseViewSet(viewsets.ModelViewSet):
    """
    List/Detail all the exercises able to be performed
    """
    permission_classes = [IsAdminOrReadOnly, TokenHasReadWriteScope]
    required_scopes = ['exercises']
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    filter_class = ExerciseFilter
