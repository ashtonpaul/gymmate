from django_filters import FilterSet, CharFilter

from .models import AccountUser


class UserFilter(FilterSet):
    """
    Filter set for account users for URL queryset
    """
    username = CharFilter(name='username', lookup_type='icontains')
    first_name = CharFilter(name='first_name', lookup_type='icontains')
    last_name = CharFilter(name='last_name', lookup_type='icontains')

    class Meta:
        model = AccountUser
        fields = ['username', 'first_name', 'last_name']
