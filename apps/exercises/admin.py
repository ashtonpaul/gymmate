from django.contrib import admin
from .models import Muscle, ExerciseCategory, Equipment, Exercise, ExerciseImage


class ExerciseAdmin(admin.ModelAdmin):
    pass

admin.site.register(ExerciseCategory, ExerciseAdmin)
admin.site.register(Equipment, ExerciseAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(ExerciseImage, ExerciseAdmin)
admin.site.register(Muscle, ExerciseAdmin)
