import logging

from django.utils.timezone import now


class LogEntry(object):
    """
    Log entry object for each log line
    """
    pass


class LoggingMixin(object):
    """
    Custom logging mixin to save logs to file
    """
    def initial(self, request, *args, **kwargs):
        self.request.log = LogEntry()
        self.request.log.logger = logging.getLogger(__name__)
        self.request.log.path = request.path
        self.request.log.remote_addr = request.META.get("HTTP_X_FORWARDED_FOR", None)
        self.request.log.host = request.get_host()
        self.request.log.method = request.method
        self.request.log.query_params = request.query_params.dict()
        self.request.log.data = request.data.dict()
        self.request.log.datetime = now()
        super(LoggingMixin, self).initial(request, *args, **kwargs)

        

    def finalize_response(self, request, response, *args, **kwargs):
        response = super(LoggingMixin, self).finalize_response(request, response, *args, **kwargs)
        # compute response time
        response_timedelta = now() - self.request.log.datetime
        response_ms = int(response_timedelta.total_seconds() * 1000)
        
        entry = self.request.log

        entry.logger.info(response_ms)
        return response