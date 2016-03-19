from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class LinkHeaderPagination(PageNumberPagination):
    """
    Custom pagination style using Links in the header instead of
    the response body similar style to the GitHub API
    """
    page_size_query_param = 'per_page'

    def get_paginated_response(self, data):
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()

        if next_url is not None and previous_url is not None:
            link = '<{next_url}>; rel="next", <{previous_url}>; rel="prev"'
        elif next_url is not None:
            link = '<{next_url}>; rel="next"'
        elif previous_url is not None:
            link = '<{previous_url}>; rel="prev"'
        else:
            link = ''

        link = link.format(next_url=next_url, previous_url=previous_url)
        headers = {'Link': link} if link else {}
        headers.update({'X-Total-Count': self.page.paginator.count})

        return Response(data, headers=headers)


class LargerLinkHeaderPagination(LinkHeaderPagination):
    """
    Same as above just for a larger page size of 100
    """
    page_size = 100
