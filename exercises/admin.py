from django.contrib import admin
from exercises.models import Muscle, ExerciseCategory, Equipment, Exercise


class ExerciseAdmin(admin.ModelAdmin):
    pass

admin.site.register(ExerciseCategory, ExerciseAdmin)
admin.site.register(Equipment, ExerciseAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Muscle, ExerciseAdmin)
