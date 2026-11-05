from rest_framework.pagination import (PageNumberPagination,
                                       LimitOffsetPagination,
                                       CursorPagination)
from rest_framework.response import Response


class BasePagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 15

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'page_size': self.page_size,
            'page': self.page.number,
            'previous': self.get_previous_link(),
            'next': self.get_next_link(),
            'results': data,
        })


# class CategoryLimitPagination(LimitOffsetPagination):
#     default_limit = 5
#     max_page_size = 10

#
# class BookCursorPagination(CursorPagination):
#     page_size = 10
#     # ordering = '-created_at'
#     ordering = ('-published_date', 'created_at')