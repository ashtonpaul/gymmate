from rest_framework.test import APITestCase, APIClient

from accounts.models import AccountUser
from metrics.models import Metric, MetricType, MetricTypeGroup


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
        AccountUser.objects.create_user(
            username=self.user_admin,
            email='admin@test.com',
            is_active=True,
            is_staff=True
        )
        AccountUser.objects.create_user(username=self.user_basic, email='user@test.com', is_active=True)

        self.client = APIClient()

    def authenticate(self, username=None):
        """
        Method to authenticate and switch currently logged in user
        """
        self.user = AccountUser.objects.get(username=username)
        self.client.force_authenticate(user=self.user)
        return self.user


class MetricsTestCase(BaseTestCase):
    def populate(self):
        """
        Common base method for populating data for testing between models
        """
        self.authenticate(self.user_admin)
        self.group = MetricTypeGroup.objects.create(name='test_group')
        self.type = MetricType.objects.create(name='test_type', unit='test', group=self.group)
        self.metric = Metric.objects.create(user=self.user, metric_type=self.type, value='1')
