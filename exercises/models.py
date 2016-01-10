from __future__ import unicode_literals

from django.db import models


class Muscle(models.Model):
    name = models.CharField(max_length=50, blank=False, help_text="Latin representation", )
    is_front = models.BooleanField(default=True)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return self.name


class ExerciseCategory(models.Model):
    name = models.CharField(max_length=50, blank=False, )

    class Meta:
        ordering = ['name', ]
        verbose_name_plural = 'Exercise Categories'

    def __str__(self):
            return self.name


class Equipment(models.Model):
    name = models.CharField(max_length=100, blank=False, )

    class Meta:
        ordering = ['name', ]
        verbose_name_plural = 'Equipment'

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ExerciseCategory, null=True)
    description = models.TextField(max_length=2000, )
    muscles = models.ManyToManyField(Muscle, blank=True, verbose_name="Primary muscles", )
    muscles_secondary = models.ManyToManyField(Muscle, blank=True,
                                               related_name='secondary_muscles', verbose_name="Secondary muscles", )
    equipment = models.ManyToManyField(Equipment, blank=True, )
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return self.name
