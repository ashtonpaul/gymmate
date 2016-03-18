from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ..core.validators import PasswordValidator

from .models import AccountUser
from .tasks import generate_thumbnail


class ThumbnailSerializer(serializers.ImageField):
    """
    Custom thumbnail serializer to return thumbnail url
    http://stackoverflow.com/questions/35834664/django-rest-framework-with-easy-thumbnails
    """
    def to_representation(self, instance):
        if instance:
            return generate_thumbnail(instance)


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
    thumb = ThumbnailSerializer(source="avatar", required=False)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(
            queryset=AccountUser.objects.all(),
            message='Email already in use by another account')]
    )

    class Meta:
        model = AccountUser
        fields = ('id', 'username', 'password', 'gender', 'email',
                  'first_name', 'last_name', 'date_joined', 'avatar', 'thumb')
        read_only_fields = ['date_joined', 'thumb', ]
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
    password = serializers.CharField(
        style={'input_type': 'password'},
        validators=[PasswordValidator()]
    )

    class Meta:
        model = AccountUser
        fields = ('email', 'password')
        write_only_fields = ('password',)


class ForgotPasswordSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer to accept email for forgotten password
    """
    email = serializers.EmailField(required=True)

    class Meta:
        model = AccountUser
        fields = ('email', )
