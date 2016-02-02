from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateTimeFilter

from .models import Metric, MetricType, MetricTypeGroup


class MetricTypeGroupFilter(FilterSet):
    """
    Filter set for metric type groups
    """
    name = CharFilter(lookup_type='icontains')

    class Meta:
        model = MetricTypeGroup
        fields = ['name', ]


class MetricTypeFilter(FilterSet):
    """
    Filter set for metric type
    """
    group = ModelChoiceFilter(queryset=MetricTypeGroup.objects.all())
    name = CharFilter(lookup_type='icontains')
    unit = CharFilter(lookup_type='icontains')

    class Meta:
        model = MetricType
        fields = ['name', 'unit']


class MetricFilter(FilterSet):
    """
    Filter Set for user metric entries
    """
    metric_type = ModelChoiceFilter(queryset=MetricType.objects.all())
    max_date = DateTimeFilter(name='date', lookup_type='lte')
    min_date = DateTimeFilter(name='date', lookup_type='gte')

    class Meta:
        model = Metric
        fields = ['metric_type', 'min_date', 'max_date']
