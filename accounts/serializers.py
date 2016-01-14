from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import AccountUser


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Generic user serializer
    """
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=AccountUser.objects.all())])

    class Meta:
        model = AccountUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name',
                  'date_joined', 'last_login', 'is_active', )
