from django.db import models
from exercises.models import Exercise
from accounts.models import AccountUser


class Routine(models.Model):
    user = models.ForeignKey(AccountUser)
    name = models.CharField(max_length=100, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    exercises = models.ManyToManyField(Exercise)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return self.name
