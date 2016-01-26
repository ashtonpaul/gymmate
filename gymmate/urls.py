from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers

from accounts.views import UserViewSet, SignUpViewSet
from metrics.views import MetricViewSet, MetricTypeViewSet, MetricTypeGroupViewSet
from exercises.views import MuscleViewSet, ExerciseCategoryViewSet, EquipmentViewSet, ExerciseViewSet
from workouts.views import DayOfWeekViewSet, PublicRoutineViewSet, RoutineViewSet, ProrgressViewSet

router = routers.DefaultRouter()
router.register(r'daysofweek', DayOfWeekViewSet, 'dayofweek')
router.register(r'equipment', EquipmentViewSet, 'equipment')
router.register(r'exercises', ExerciseViewSet, 'exercise')
router.register(r'exercise-categories', ExerciseCategoryViewSet, 'exercise-category')
router.register(r'metrics', MetricViewSet, 'metric')
router.register(r'metrics-type', MetricTypeViewSet, 'metric-type')
router.register(r'metrics-type-group', MetricTypeGroupViewSet, 'metric-group')
router.register(r'muscles', MuscleViewSet, 'muscle')
router.register(r'progress', ProrgressViewSet, 'progress')
router.register(r'public-routines', PublicRoutineViewSet, 'public-routine')
router.register(r'routines', RoutineViewSet, 'routine')
router.register(r'signup', SignUpViewSet, 'signup')
router.register(r'users', UserViewSet, 'user')

# Wire up our API using automatic URL routing.
urlpatterns = [
    url(r'^', include(router.urls)),
]

# Administrative panel
urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
]

# Documentaton views for API
urlpatterns += [
    url(r'^docs/', include('rest_framework_swagger.urls', namespace='rest_framework_swagger')),
]

# Oauth endpoint
urlpatterns += [
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
