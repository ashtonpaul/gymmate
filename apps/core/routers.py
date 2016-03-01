from rest_framework.routers import DefaultRouter
from ..core.loggers import LoggingMixin


class CustomRouter(DefaultRouter):
    """
    Extend DefaultRouter to allow for root level logging
    """
    def get_api_root_view(self):
        api_root_view = super(CustomRouter, self).get_api_root_view()
        ApiRootClass = api_root_view.cls

        class APIRoot(LoggingMixin, ApiRootClass):
            pass

        return APIRoot.as_view()
