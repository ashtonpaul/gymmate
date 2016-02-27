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
    logging_exclude = None

    def initial(self, request, *args, **kwargs):
        ip = request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        data = request.data if type(request.data).__name__ == 'dict' else request.data.dict()

        # exclusion of fields in log data e.g passwords
        if self.logging_exclude:
            for key in self.logging_exclude:
                data.pop(key, None)

        self.request.log = LogEntry()
        self.request.log.logger = logging.getLogger(__name__)
        self.request.log.path = request.path
        self.request.log.ip = ip.split(", ")[0]
        self.request.log.method = request.method
        self.request.log.params = request.query_params.dict()
        self.request.log.data = data
        self.request.log.timestamp = now()

        super(LoggingMixin, self).initial(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        """
        Return the response and send log information to log handler
        """
        response = super(LoggingMixin, self).finalize_response(request, response, *args, **kwargs)

        details = {
            'response_time': int((now() - self.request.log.timestamp).total_seconds() * 1000),
            'stamp': self.request.log.timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
            'user': request.user,
            'ip': self.request.log.ip,
            'path': self.request.log.path,
            'method': self.request.log.method,
            'params': self.request.log.params,
            'status_code': response.status_code,
            'data': self.request.log.data,
            'response': response.rendered_content,
        }
        self.request.log.logger.info('', extra=details)

        return response
