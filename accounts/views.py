from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import AccountUser
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (AllowAny, )
    queryset = AccountUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

    def destroy(self, request, *args, **kwargs):
        """
        return a 405 response if user tries to delete a profile other than theirs
        """
        instance = self.get_object()
        if (instance.username == request.user.username):
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        """
        return a 405 response if user tries to update a profile other than theirs
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if (instance.username == request.user.username):
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
