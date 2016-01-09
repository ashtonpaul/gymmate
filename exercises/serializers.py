from rest_framework import serializers
from .models import Muscle, ExerciseCategory, Equipment, Exercise


class MuscleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Muscle
        fields = ('id', 'name', 'is_front', )


class ExerciseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseCategory
        fields = ('id', 'name', )


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ('id', 'name', )


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
