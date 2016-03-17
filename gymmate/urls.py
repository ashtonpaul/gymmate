from django.conf.urls import url, include, patterns
from django.contrib import admin
from django.conf import settings

from apps.core.routers import CustomRouter
from rest_framework_swagger import urls as documentaton
from oauth2_provider import urls as authentication

from apps.accounts.views import UserViewSet, SignUpViewSet, ForgotPasswordViewSet, ActivateView, ResetView
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
router.register(r'users', UserViewSet, 'user')

# user account/password handling
router.register(r'signup', SignUpViewSet, 'signup')
router.register(r'forgot-password', ForgotPasswordViewSet, 'forgot-password')

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
    url(r'^v1/docs/', include(documentaton, namespace='rest_framework_swagger')),
]

# Oauth endpoint
urlpatterns += [
    url(r'^o/', include(authentication, namespace='oauth2_provider')),
]

# activate and reset password urls
urlpatterns += [
    url(r'^a/(?P<uuid>[^/]+)/$', ActivateView, name='activate_view'),
    url(r'^r/(?P<uuid>[^/]+)/$', ResetView, name='reset_view'),
]

# status files
urlpatterns += patterns(
    '',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
