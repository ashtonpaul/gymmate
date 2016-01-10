from django.db import models
from exercises.models import Exercise
from accounts.models import AccountUser


class DaysOfWeek(models.Model):
    day = models.CharField(max_length=9, blank=False, null=False)

    def __str__(self):
        return self.day


class Routine(models.Model):
    user = models.ForeignKey(AccountUser)
    name = models.CharField(max_length=100, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    exercises = models.ManyToManyField(Exercise)
    days = models.ManyToManyField(DaysOfWeek)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return self.name
