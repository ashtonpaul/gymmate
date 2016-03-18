from django.contrib import admin
from .models import DayOfWeek, Routine, Progress, Set


class WorkoutAdmin(admin.ModelAdmin):
    pass

admin.site.register(DayOfWeek, WorkoutAdmin)
admin.site.register(Routine, WorkoutAdmin)
admin.site.register(Progress, WorkoutAdmin)
admin.site.register(Set, WorkoutAdmin)
