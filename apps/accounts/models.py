import uuid
from os.path import splitext

from django.contrib.auth.models import User, UserManager
from django.db import models


def upload_to(instance, filename):
    '''
    Returns the upload target for profile pictures
    '''
    filename, file_extension = splitext(filename)
    folder = instance.uuid.hex
    filename = str(uuid.uuid4()) + file_extension
    return "profile-pictures/{0}/{1}".format(folder, filename)


class AccountUser(User):
    """
    Abstract class of built-in django User Model
    """
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_activated = models.BooleanField(default=False)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, blank=True)
    gym = models.CharField(max_length=200, blank=True)
    date_of_birth = models.DateField(blank=True, null=True,)
    avatar = models.ImageField(blank=True, upload_to=upload_to, )

    objects = UserManager()

    class Meta:
        verbose_name = 'user'

    def __str__(self):
        return '%s' % (self.username)

    @property
    def full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        """
        Save profile picture, if update remove old file
        """
        try:
            this = AccountUser.objects.get(id=self.id)
            if this.avatar != self.avatar:
                this.avatar.delete(save=False)
        except:
            pass

        super(AccountUser, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        If profile picture exists delete before entry removal
        """
        try:
            storage, path = self.avatar.storage, self.avatar.path
            storage.delete(path)
        except:
            pass
        super(AccountUser, self).delete(*args, **kwargs)
