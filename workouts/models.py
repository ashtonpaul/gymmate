from django.db import models

from exercises.models import Exercise
from accounts.models import AccountUser


class DayOfWeek(models.Model):
    """
    Days of the week
    """
    day = models.CharField(max_length=9, blank=False, null=False)

    def __str__(self):
        return self.day


class Routine(models.Model):
    """
    Allow users to group exercises into routines
    """
    user = models.ForeignKey(AccountUser)
    name = models.CharField(max_length=100, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    exercises = models.ManyToManyField(Exercise)
    days = models.ManyToManyField(DayOfWeek, blank=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return self.name


class Progress(models.Model):
    """
    Track user progress for exercises completed
    """
    exercise = models.ForeignKey(Exercise, null=False)
    user = models.ForeignKey(AccountUser, null=False)
    date = models.DateField(auto_now_add=False)
    duration = models.IntegerField()
    Sets = models.IntegerField()
    reps = models.IntegerField()
    weight = models.IntegerField()

    class Meta:
        ordering = ['date', 'exercise']

    def __str__(self):
        return ('%s - %s' % (self.exercise, self.date.strftime('%m/%d/%Y')))
