from rest_framework import viewsets
from .models import AccountUser
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = AccountUser.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
