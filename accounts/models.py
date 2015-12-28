from django.contrib.auth.models import User, UserManager


class AccountUser(User):
    objects = UserManager()

    class Meta:
        verbose_name = 'user'

    def __str__(self):
        return '%s' % (self.username)
