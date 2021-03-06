from django.db import models

from ..exercises.models import Exercise
from ..accounts.models import AccountUser


class DayOfWeek(models.Model):
    """
    Days of the week
    """
    day = models.CharField(max_length=9, unique=True)

    def __str__(self):
        return self.day


class RoutineManager(models.Manager):
    """
    Custom Routine manager
    """
    def public(self):
        """
        Filter all routines that are marked for public viewing
        """
        return self.filter(is_public=True)


class Routine(models.Model):
    """
    Allow users to group exercises into routines
    """
    user = models.ForeignKey(AccountUser, null=True)
    name = models.CharField(max_length=100, )
    description = models.TextField(max_length=300, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    exercises = models.ManyToManyField(Exercise)
    days = models.ManyToManyField(DayOfWeek, blank=True)
    is_public = models.BooleanField(default=False)

    objects = RoutineManager()

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return self.name


class Progress(models.Model):
    """
    Track user progress for exercises completed
    """
    exercise = models.ForeignKey(Exercise)
    user = models.ForeignKey(AccountUser)
    date = models.DateField(auto_now_add=False)

    class Meta:
        ordering = ['date', 'exercise']

    def __str__(self):
        return ('%s - %s' % (self.exercise, self.date.strftime('%m/%d/%Y')))


class Set(models.Model):
    """
    Dynamic sets for each progress
    """
    progress = models.ForeignKey(Progress)
    duration = models.IntegerField(null=True)
    reps = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
