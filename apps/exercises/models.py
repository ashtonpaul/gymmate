from django.db import models


class Muscle(models.Model):
    """
    Model for muscles storing location and latin name also
    """
    latin_name = models.CharField(max_length=50, blank=True, help_text="Latin representation", )
    name = models.CharField(max_length=50, blank=False, help_text="Muscle name e.g biceps", )
    is_front = models.BooleanField(default=True)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return self.name


class ExerciseCategory(models.Model):
    """
    Different exercise categories to subclass exercises
    """
    name = models.CharField(max_length=50, blank=False, )

    class Meta:
        ordering = ['name', ]
        verbose_name_plural = 'Exercise Categories'

    def __str__(self):
            return self.name


class Equipment(models.Model):
    """
    Equipment that can usually be found in a gym
    """
    name = models.CharField(max_length=100, blank=False, )

    class Meta:
        ordering = ['name', ]
        verbose_name_plural = 'Equipment'

    def __str__(self):
        return self.name


class Exercise(models.Model):
    """
    Exercise model with details about exercises that can be performed
    """
    name = models.CharField(max_length=200)
    category = models.ForeignKey(ExerciseCategory, null=True)
    description = models.TextField(max_length=2000, )
    muscles = models.ManyToManyField(Muscle, blank=True, verbose_name="Primary muscles", )
    muscles_secondary = models.ManyToManyField(Muscle, blank=True,
                                               related_name='secondary_muscles', verbose_name="Secondary muscles", )
    equipment = models.ManyToManyField(Equipment, blank=True, )
    date_created = models.DateTimeField(auto_now_add=True)
    is_cardio = models.BooleanField(default=False)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return self.name
