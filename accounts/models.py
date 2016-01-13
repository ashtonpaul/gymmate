from django.contrib.auth.models import User, UserManager


class AccountUser(User):
    """
    Abstract class of built-in django User Model
    """    
    objects = UserManager()

    class Meta:
        verbose_name = 'user'

    def __str__(self):
        return '%s' % (self.username)
