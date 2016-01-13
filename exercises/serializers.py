from rest_framework import serializers

from .models import Muscle, ExerciseCategory, Equipment, Exercise


class MuscleSerializer(serializers.ModelSerializer):
    """
    Muscle serializer
    """
    class Meta:
        model = Muscle


class ExerciseCategorySerializer(serializers.ModelSerializer):
    """
    Exercise groups/category serializer
    """
    class Meta:
        model = ExerciseCategory


class EquipmentSerializer(serializers.ModelSerializer):
    """
    Gym equipment serializer
    """
    class Meta:
        model = Equipment


class ExerciseSerializer(serializers.ModelSerializer):
    """
    Exercises serializer
    """
    class Meta:
        model = Exercise
