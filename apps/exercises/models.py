from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Muscle(models.Model):
    """
    Model for muscles storing location and latin name also
    """
    latin_name = models.CharField(max_length=50, blank=True, help_text="Latin representation", )
    name = models.CharField(max_length=50, help_text="Muscle name e.g biceps", )
    is_front = models.BooleanField(default=True)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return self.name


class ExerciseCategory(models.Model):
    """
    Different exercise categories to subclass exercises
    """
    name = models.CharField(max_length=50, )

    class Meta:
        ordering = ['name', ]
        verbose_name_plural = 'Exercise Categories'

    def __str__(self):
            return self.name


class Equipment(models.Model):
    """
    Equipment that can usually be found in a gym
    """
    name = models.CharField(max_length=100, )

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
    video = models.URLField(blank=True, )
    date_created = models.DateTimeField(auto_now_add=True)
    is_cardio = models.BooleanField(default=False)

    class Meta:
        ordering = ['name', ]

    def __str__(self):
        return self.name


def upload_to(instance, filename):
    '''
    Returns the upload target for exercise images
    '''
    return "exercises/{0}/{1}".format(instance.exercise.id, filename)


class ExerciseImage(models.Model):
    """
    Exercise images for individual exercises
    """
    exercise = models.ForeignKey(Exercise, related_name='images')
    image = models.ImageField(upload_to=upload_to, )
    is_main = models.BooleanField(default=False, )

    class Meta:
        ordering = ['exercise', '-is_main']
        verbose_name_plural = 'Exercise Images'

    def __str__(self):
        exercise = Exercise.objects.get(id=self.exercise.id)
        return '{0} - {1}'.format(exercise, self.image)

    def save(self, *args, **kwargs):
        """
        Only one is_main image can exist per exercise
        """
        if self.is_main and ExerciseImage.objects.filter(exercise=self.exercise, is_main=True).count():
            ExerciseImage.objects.filter(exercise=self.exercise).update(is_main=False)

        super(ExerciseImage, self).save(*args, **kwargs)
        check_is_main(self.exercise.id)


def check_is_main(exercise):
    """
    Check if an exercise has a main image, if not then default the first image as main
    """
    if (not ExerciseImage.objects.filter(exercise=exercise, is_main=True).count() and
       ExerciseImage.objects.filter(exercise=exercise, is_main=False).count() != 0):
        image = ExerciseImage.objects.filter(exercise=exercise, is_main=False)[0]
        image.is_main = True
        image.save()


@receiver(post_delete, sender=ExerciseImage)
def exercise_image_post_delete(sender, **kwargs):
    """
    Post delete hook to remove the physical file
    """
    file = kwargs['instance']
    storage = file.image.storage
    path = file.image.path
    storage.delete(path)
    check_is_main(file.exercise.id)
