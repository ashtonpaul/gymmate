import uuid

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..core.permissions import IsCreateOnly
from ..core.loggers import LoggingMixin
from ..core.mail import send_email

from .models import AccountUser
from .filters import UserFilter
from .serializers import UserSerializer, SignUpSerializer, ForgotPasswordSerializer, ResetPasswordSerializer


class UserViewSet(LoggingMixin, viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed
    """
    permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    required_scopes = ['accounts']
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
            message = {"detail": "Not allowed to create new users"}
            return Response(message, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        """
        return a 405 response if regular user tries to delete a profile other than theirs
        """
        instance = self.get_object()
        if (instance.username == request.user.username) or (request.user.is_staff):
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            message = {"detail": "Not allowed to delete a different user's profile"}
            return Response(message, status=status.HTTP_405_METHOD_NOT_ALLOWED)

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
            message = {"detail": "Not allowed to update a different user's profile"}
            return Response(message, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class SignUpViewSet(LoggingMixin, viewsets.ModelViewSet):
    """
    API endpoint to allow users to sign up
    """
    permission_classes = (IsCreateOnly, )
    queryset = AccountUser.objects.all()
    serializer_class = SignUpSerializer
    http_method_names = ['post', 'head', 'options']
    logging_exclude = ['password']

    def create(self, request, *args, **kwargs):
        """
        On create, remove password hash in response and email user
        """
        # save user to database
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # send out welcome/actication email to user
        user_email = serializer.data["email"]
        uuid = str(AccountUser.objects.get(email=user_email).uuid)
        template_data = {"email": user_email, "uuid": uuid}
        send_email(user_email, 'gymmate-welcome', template_data,)

        # return success message in signup response
        success_message = {"detail": u"User successfully created."}
        headers = self.get_success_headers(serializer.data)
        return Response(success_message, status=status.HTTP_201_CREATED, headers=headers)


class ForgotPasswordViewSet(LoggingMixin, viewsets.ModelViewSet):
    """
    Allow a user to request a password reset url
    """
    permission_classes = (AllowAny, )
    queryset = AccountUser.objects.all()
    serializer_class = ForgotPasswordSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """
        Send email to user with reset url
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = AccountUser.objects.get(email=serializer.data["email"])
        except:
            user = None

        # TODO
        # Create unique reset string
        if user:
            user.uuid = uuid.uuid4()
            user.save()
            template_data = {"email": user.email, "uuid": str(user.uuid)}
            send_email(user.email, 'gymmate-forgot', template_data)

        message = {"detail": "Password reset instructions have been sent to your email"}
        headers = self.get_success_headers(serializer.data)
        return Response(message, status=status.HTTP_201_CREATED, headers=headers)


class ResetPasswordViewSet(LoggingMixin, viewsets.ModelViewSet):
    """
    Allow a user to be able to reset their password
    """
    permission_classes = (AllowAny, )
    queryset = AccountUser.objects.all()
    serializer_class = ResetPasswordSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        """
        Ability to reset a user password
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        message = {"detail": "Your password has sucessfully been updated"}
        status_code = status.HTTP_200_OK

        try:
            user = AccountUser.objects.get(email=serializer.data["email"])
        except:
            user = None

        # if user not found
        if not user:
            message = {"detail": "User not found"}
            status_code = status.HTTP_400_BAD_REQUEST

        # if the reset_code doesn't match the email
        if user and str(user.uuid) != request.META.get('HTTP_RESET_CODE'):
            message = {"detail": "Not authorized to reset password for this account"}
            status_code = status.HTTP_400_BAD_REQUEST

        # if the passwords do not match
        if serializer.data["password"] != serializer.data["confirm_password"]:
            message = {"detail": "Password(s) entered do no match"}
            status_code = status.HTTP_400_BAD_REQUEST

        # Reset password if validated and notify user
        if user and status_code == status.HTTP_200_OK:
            user.set_password(serializer.data["password"])
            user.is_activated = True
            user.uuid = uuid.uuid4()
            user.save()

            template_data = {"email": user.email}
            send_email(user.email, 'gymmate-reset', template_data)

        return Response(message, status=status_code, headers=headers)
