from datetime import timedelta

from django.utils import timezone

from rest_framework.test import APITestCase, APIClient

from oauth2_provider.models import AccessToken, get_application_model

from ..accounts.models import AccountUser
from ..metrics.models import Metric, MetricType, MetricTypeGroup

# Return the Application model that is active in this project.
# http://bit.do/bKFJB
Application = get_application_model()


class BaseTestCase(APITestCase):
    """
    Base Test Case extends APITestCase for authentication in other tests
    """
    # Test user accounts
    user_admin = 'admin'
    user_basic = 'user'

    def setUp(self):
        """
        Set up user for authentication to run tests
        """
        app_owner = AccountUser.objects.create_user(
            username=self.user_admin,
            email='admin@test.com',
            is_active=True,
            is_staff=True
        )
        AccountUser.objects.create_user(username=self.user_basic, email='user@test.com', is_active=True)

        self.application = Application.objects.create(
            name="Test Application",
            redirect_uris="http://localhost",
            user=app_owner,
            client_type=Application.CLIENT_PUBLIC,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )

        self.client = APIClient()

    def create_authorization_header(self, token):
        """
        Format token to be accepted in header
        """
        return "Bearer {0}".format(token)

    def authenticate(self, username=None):
        """
        Method to authenticate and switch currently logged in user
        """
        self.user = AccountUser.objects.get(username=username)

        self.access_token = AccessToken.objects.create(
            user=self.user,
            scope='read write exercises metrics workouts accounts',
            expires=timezone.now() + timedelta(seconds=300),
            token=username,
            application=self.application
        )

        self.auth = self.create_authorization_header(self.access_token.token)
        self.client.credentials(HTTP_AUTHORIZATION=self.auth)

        return self.user


class MetricsTestCase(BaseTestCase):
    """
    Base test case for user metrics
    """
    def populate(self):
        """
        Common base method for populating data for testing between models
        """
        self.authenticate(self.user_admin)
        self.group = MetricTypeGroup.objects.create(name='test_group')
        self.type = MetricType.objects.create(name='test_type', unit='test', group=self.group)
        self.metric = Metric.objects.create(user=self.user, metric_type=self.type, value='1')
