from rest_framework import serializers
from .models import DayOfWeek, Routine, Progress


class DayOfWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayOfWeek


class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        exclude = ('user', )


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        exclude = ('user', )
