# PYTHON IMPORTS
from collections import OrderedDict

# DJANGO REST FRAMEWORK IMPORTS
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ListPostsCommentsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('current_page', self.page.number),
            ('total_pages', self.page.paginator.num_pages),
            ('total_count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
    

class ListLikesPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('current_page', self.page.number),
            ('total_pages', self.page.paginator.num_pages),
            ('total_count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))
