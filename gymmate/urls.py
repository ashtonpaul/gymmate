from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from accounts.views import UserViewSet
from metrics.views import MetricViewSet, MetricTypeViewSet, MetricTypeGroupViewSet
from exercises.views import MuscleViewSet, ExerciseCategoryViewSet, EquipmentViewSet, ExerciseViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'user')
router.register(r'metrics', MetricViewSet, 'metric')
router.register(r'metrics-type', MetricTypeViewSet, 'metric-type')
router.register(r'metrics-type-group', MetricTypeGroupViewSet, 'metric-group')
router.register(r'exercises', ExerciseViewSet, 'exercise')
router.register(r'exercise-categories', ExerciseCategoryViewSet, 'exercise-category')
router.register(r'muscles', MuscleViewSet, 'muscle')
router.register(r'equipment', EquipmentViewSet, 'equipment')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# Login and logout views for the browsable API
urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
]
