from rest_framework import serializers

from .models import AccountUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Generic user serializer
    """
    class Meta:
        model = AccountUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'date_joined', 'last_login', 'is_active', )
