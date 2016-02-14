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

        try:
            data_dict = request.data.dict()
        except AttributeError:  # if already a dict, can't dictify
            data_dict = request.data

        ipaddr = request.META.get("HTTP_X_FORWARDED_FOR", None)
        if ipaddr:
            # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
            ipaddr = ipaddr.split(", ")[0]
        else:
            ipaddr = request.META.get("REMOTE_ADDR", "")

        self.request.log = LogEntry()
        self.request.log.logger = logging.getLogger(__name__)
        self.request.log.path = request.path
        self.request.log.ip = ipaddr
        self.request.log.method = request.method
        self.request.log.params = request.query_params.dict()
        self.request.log.data = data_dict
        self.request.log.date = now()
        super(LoggingMixin, self).initial(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        response = super(LoggingMixin, self).finalize_response(request, response, *args, **kwargs)
        entry = self.request.log

        # compute response time
        response_timedelta = now() - entry.date
        response_time = int(response_timedelta.total_seconds() * 1000)

        details = {
            'date': entry.date.strftime('%Y-%m-%d %H:%M:%S'),
            'user': request.user,
            'ip': entry.ip,
            'path': entry.path,
            'method': entry.method,
            'params': entry.params,
            'status_code': response.status_code,
            'response_time': response_time,
            'data': entry.data,
            'response': response.rendered_content,
        }

        entry.logger.info('', extra=details)
        return response
