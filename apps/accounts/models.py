import uuid
import hashlib
from os.path import splitext

from django.contrib.auth.models import User, UserManager
from django.db import models


def upload_to(instance, filename):
    '''
    Returns the upload target for profile pictures
    '''
    filename, file_extension = splitext(filename)
    folder = hashlib.md5(instance.uuid.hex).hexdigest()
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
    profile_picture = models.ImageField(blank=True, upload_to=upload_to, )

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
        Delete old file when replaceing by updating file
        """
        try:
            this = AccountUser.objects.get(id=self.id)
            if this.profile_picture != self.profile_picture:
                this.profile_picture.delete(save=False)
        except:
            pass

        super(AccountUser, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Delete image file upon object deletion
        """
        storage, path = self.profile_picture.storage, self.profile_picture.path
        super(AccountUser, self).delete(*args, **kwargs)

        storage.delete(path)