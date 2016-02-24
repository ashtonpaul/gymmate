from rest_framework import serializers

from .models import Muscle, ExerciseCategory, Equipment, Exercise, ExerciseImage


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


class ExerciseImageSerializer(serializers.ModelSerializer):
    """
    Gym equipment serializer
    """
    class Meta:
        model = ExerciseImage
        fields = ('image', 'is_main', )


class ExerciseSerializer(serializers.ModelSerializer):
    """
    Exercises serializer
    """
    images = ExerciseImageSerializer(many=True, read_only=True)

    class Meta:
        model = Exercise
