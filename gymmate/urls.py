from django.conf.urls import url, include
from django.contrib import admin

from apps.core.routers import CustomRouter

from apps.accounts.views import UserViewSet, SignUpViewSet, ForgotPasswordViewSet
from apps.metrics.views import MetricViewSet, MetricTypeViewSet, MetricTypeGroupViewSet
from apps.exercises.views import MuscleViewSet, ExerciseCategoryViewSet, EquipmentViewSet, ExerciseViewSet
from apps.workouts.views import DayOfWeekViewSet, PublicRoutineViewSet, RoutineViewSet, ProrgressViewSet


router = CustomRouter()
router.register(r'daysofweek', DayOfWeekViewSet, 'dayofweek')
router.register(r'equipment', EquipmentViewSet, 'equipment')
router.register(r'exercises', ExerciseViewSet, 'exercise')
router.register(r'exercise-categories', ExerciseCategoryViewSet, 'exercise-category')
router.register(r'metrics', MetricViewSet, 'metric')
router.register(r'metric-types', MetricTypeViewSet, 'metric-type')
router.register(r'metric-type-groups', MetricTypeGroupViewSet, 'metric-group')
router.register(r'muscles', MuscleViewSet, 'muscle')
router.register(r'progress', ProrgressViewSet, 'progress')
router.register(r'public-routines', PublicRoutineViewSet, 'public-routine')
router.register(r'routines', RoutineViewSet, 'routine')
router.register(r'signup', SignUpViewSet, 'signup')
router.register(r'forgot-password', ForgotPasswordViewSet, 'forgot-password')
router.register(r'users', UserViewSet, 'user')

# Wire up our API using automatic URL routing.
urlpatterns = [
    url(r'^v1/', include(router.urls, namespace='v1')),
]

# Administrative panel
urlpatterns += [
    url(r'^admin/', include(admin.site.urls)),
]

# Documentaton views for API
urlpatterns += [
    url(r'^v1/docs/', include('rest_framework_swagger.urls', namespace='rest_framework_swagger')),
]

# Oauth endpoint
urlpatterns += [
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
