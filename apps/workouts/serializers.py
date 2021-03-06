from rest_framework import serializers

from ..core.validators import FutureDateValidator

from .models import DayOfWeek, Routine, Progress, Set


class DayOfWeekSerializer(serializers.ModelSerializer):
    """
    Day of the week serializer
    """
    class Meta:
        model = DayOfWeek


class PublicRoutineSerializer(serializers.ModelSerializer):
    """
    Publically shared routines serializer
    """
    class Meta:
        model = Routine
        fields = ('id', 'user', 'name', 'date_created', 'exercises', 'days')


class RoutineSerializer(serializers.ModelSerializer):
    """
    User custom routine serializer
    """
    class Meta:
        model = Routine
        exclude = ('user', )


class SetSerializer(serializers.ModelSerializer):
    """
    Sub serializer for sets that belong to progress
    """
    class Meta:
        model = Set
        fields = ('id', 'progress', 'reps', 'weight', 'duration')


class ProgressSerializer(serializers.ModelSerializer):
    """
    User progress serializer
    """
    date = serializers.DateField(validators=[FutureDateValidator()])

    class Meta:
        model = Progress
        fields = ('id', 'date', 'exercise')
