from django_filters import FilterSet, CharFilter, BooleanFilter, ModelChoiceFilter, DateFilter

from ..exercises.models import Exercise

from .models import DayOfWeek, Routine, Progress


class DayOfWeekFilter(FilterSet):
    """
    Filter set for days of the week
    """
    day = CharFilter(lookup_type='icontains')

    class Meta:
        model = DayOfWeek
        fields = ['day', ]


class RoutineFilter(FilterSet):
    """
    Filter set for user routines
    """
    name = CharFilter(lookup_type='icontains')
    days = ModelChoiceFilter(queryset=DayOfWeek.objects.all())
    exercises = ModelChoiceFilter(queryset=Exercise.objects.all())
    is_public = BooleanFilter()

    class Meta:
        model = Routine
        fields = ['name', 'is_public', 'days', 'exercises']


class ProgressFilter(FilterSet):
    """
    Filter set for user progress entries
    """
    exercise = ModelChoiceFilter(queryset=Exercise.objects.all())
    max_date = DateFilter(name='date', lookup_type='lte')
    min_date = DateFilter(name='date', lookup_type='gte')

    class Meta:
        model = Progress
        fields = ['exercise', 'max_date', 'min_date']
