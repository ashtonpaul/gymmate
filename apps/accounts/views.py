from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope

from django.core.mail import send_mail

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from ..core.permissions import IsCreateOnly
from ..core.loggers import LoggingMixin

from .models import AccountUser
from .filters import UserFilter
from .serializers import UserSerializer, SignUpSerializer


class UserViewSet(LoggingMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed
    """
    permission_classes = (AllowAny, TokenHasReadWriteScope)
    queryset = AccountUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    filter_class = UserFilter
    http_method_names = ['get', 'delete', 'put', 'patch', 'head', 'options']

    def create(self, request, *args, **kwargs):
        """
        Do not allow current users of the system to create new users
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        if not request.user.username:
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        """
        return a 405 response if regular user tries to delete a profile other than theirs
        """
        instance = self.get_object()
        if (instance.username == request.user.username) or (request.user.is_staff):
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        """
        return a 405 response if regular user tries to update a profile other than theirs
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if (instance.username == request.user.username) or (request.user.is_staff):
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SignUpViewSet(viewsets.ModelViewSet):
    """
    API endpoint to allow users to sign up
    """
    permission_classes = (IsCreateOnly, )
    queryset = AccountUser.objects.all()
    serializer_class = SignUpSerializer
    http_method_names = ['post', 'head', 'options']

    def create(self, request, *args, **kwargs):
        """
        On create, remove password hash in response and email user
        """
        send_mail(
            subject='hello from sparkpost',
            message='Hello Rock stars!',
            from_email='ashton@ashtonpaul.com',
            recipient_list=['ashton.paul@gmail.com'],
            html_message='<p>Hello Rock stars!</p>',
        )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        success_message = {"detail": u"User successfully created."}

        return Response(success_message, status=status.HTTP_201_CREATED, headers=headers)
