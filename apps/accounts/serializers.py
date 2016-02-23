from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import AccountUser


class BaseAccountSerializer(serializers.HyperlinkedModelSerializer):
    """
    Base user account serializer
    """
    def create(self, validated_data):
        """
        Custom create function to include token creation and password hashing
        """
        first_name = validated_data['first_name'] if 'first_name' in validated_data else ''
        last_name = validated_data['last_name'] if 'last_name' in validated_data else ''

        user = AccountUser(
            email=validated_data['email'],
            username=validated_data['email'],
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(BaseAccountSerializer):
    """
    Generic user serializer
    """
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=AccountUser.objects.all())])
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=AccountUser.objects.all(),
            message='Email already in use by another account')]
    )

    class Meta:
        model = AccountUser
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'date_joined', )
        read_only_fields = ('date_joined', )
        extra_kwargs = {'password': {'write_only': True}}


class SignUpSerializer(BaseAccountSerializer):
    """
    Sign up serializer for applications
    """
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=AccountUser.objects.all(),
            message='Email already in use by another account')]
    )

    class Meta:
        model = AccountUser
        fields = ('email', 'password')
        write_only_fields = ('password',)
