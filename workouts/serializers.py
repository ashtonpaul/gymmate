from rest_framework import serializers

from .models import DayOfWeek, Routine, Progress


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


class ProgressSerializer(serializers.ModelSerializer):
    """
    User progress serializer
    """
    class Meta:
        model = Progress
        exclude = ('user', )
