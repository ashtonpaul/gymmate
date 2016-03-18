import uuid

from django.shortcuts import render
from django.core.urlresolvers import reverse
from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope

from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from ..core.permissions import IsCreateOnly
from ..core.loggers import LoggingMixin

from .tasks import send_email
from .forms import PasswordResetForm
from .models import AccountUser
from .filters import UserFilter
from .serializers import UserSerializer, SignUpSerializer, ForgotPasswordSerializer


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
        send_email.delay(user_email, 'gymmate-welcome', template_data,)

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
            send_email.delay(user.email, 'gymmate-forgot', template_data)

        message = {"detail": "Password reset instructions have been sent to your email"}
        headers = self.get_success_headers(serializer.data)
        return Response(message, status=status.HTTP_201_CREATED, headers=headers)


def AccountError(request, method):
    """
    Template view for handling user errors
    """
    return render(request, 'error.html', {'method': method})


def ActivateView(request, **kwargs):
    """
    Template view to allow users to activate their account
    """
    # if user is associated with given uuid
    try:
        url_uuid = kwargs.pop('uuid')
        url_email = request.GET.get('q', '')
        user = AccountUser.objects.get(uuid=url_uuid)
    except:
        return AccountError(request, 'activate')

    # uuid and email match user to prevent random email reset
    if user.email != url_email:
        return AccountError(request, 'activate')

    user.is_activated = True
    user.uuid = uuid.uuid4()
    user.save()

    return render(request, 'activate.html', {'email': user.email})


def ResetSuccess(request, email):
    """
    Template view to show user has successfully update password
    """
    return render(request, 'success.html', {'email': email})


def ResetView(request, **kwargs):
    """
    Allow a user to be able to reset their password
    """
    # if user is associated with given uuid
    try:
        url_uuid = kwargs.pop('uuid')
        url_email = request.GET.get('q', '')
        user = AccountUser.objects.get(uuid=url_uuid)
    except:
        return AccountError(request, 'reset')

    # uuid and email match user to prevent random email reset
    if user.email != url_email:
        return AccountError(request, 'reset')

    action = reverse('reset_view', kwargs={'uuid': url_uuid}) + '?q=' + url_email

    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            user.set_password(password)
            user.is_activated = True
            user.uuid = uuid.uuid4()
            user.save()

            template_data = {"email": user.email}
            send_email.delay(user.email, 'gymmate-reset', template_data)

            return ResetSuccess(request, user.email)
    else:
        form = PasswordResetForm()

    context = {'form': form, 'email': user.email, 'uuid': url_uuid, 'action': action}
    return render(request, 'reset.html', context)
