from django_filters import FilterSet, CharFilter, ModelChoiceFilter, BooleanFilter

from .models import Muscle, ExerciseCategory, Equipment, Exercise


class MuscleFilter(FilterSet):
    """
    Filter set for muscles
    """
    name = CharFilter(lookup_type='icontains')
    latin_name = CharFilter(lookup_type='icontains')

    class Meta:
        model = Muscle
        fields = ['name', 'latin_name']


class ExerciseCategoryFilter(FilterSet):
    """
    Filter set for exercise categories
    """
    name = CharFilter(lookup_type='icontains')

    class Meta:
        model = ExerciseCategory
        fields = ['name', ]


class EquipmentFilter(FilterSet):
    """
    Filter set for exercise categories
    """
    name = CharFilter(lookup_type='icontains')
    is_machine = BooleanFilter()

    class Meta:
        model = Equipment
        fields = ['name', 'is_machine']


class ExerciseFilter(FilterSet):
    """
    Filter set for exercise categories
    """
    name = CharFilter(lookup_type='icontains')
    category = ModelChoiceFilter(queryset=ExerciseCategory.objects.all())
    muscles = ModelChoiceFilter(queryset=Muscle.objects.all())
    is_cardio = BooleanFilter()

    class Meta:
        model = Exercise
        fields = ['name', 'category', 'muscles', 'is_cardio']
