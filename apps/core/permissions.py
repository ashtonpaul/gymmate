from rest_framework.permissions import BasePermission

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']
CREATE_ONLY_METHODS = ['POST', 'HEAD', 'OPTIONS']

class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as an admin, or is a read-only request.
    """

    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or
           request.user and
           request.user.is_staff):
            return True
        return False


class IsCreateOnly(BasePermission):
    """
    The request is by a user looking to sign up to the API
    """
    def has_permission(self, request, view):
        if request.method in CREATE_ONLY_METHODS:
            return True
        else:
            return False
