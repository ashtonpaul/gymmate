from django.contrib import admin
from metrics.models import Metric, MetricType, MetricTypeGroup


class MetricAdmin(admin.ModelAdmin):
    pass

admin.site.register(MetricTypeGroup, MetricAdmin)
admin.site.register(MetricType, MetricAdmin)
admin.site.register(Metric, MetricAdmin)
