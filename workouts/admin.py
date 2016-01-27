from django.contrib import admin
from workouts.models import DayOfWeek, Routine, Progress


class WorkoutAdmin(admin.ModelAdmin):
    pass

admin.site.register(DayOfWeek, WorkoutAdmin)
admin.site.register(Routine, WorkoutAdmin)
admin.site.register(Progress, WorkoutAdmin)
