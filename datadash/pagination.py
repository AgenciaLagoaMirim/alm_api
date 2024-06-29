from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StationReadingsSensorsPagination(PageNumberPagination):
    page_size = 500
    page_size_query_param = "size"


class StationReadingsPagination(PageNumberPagination):
    page_size = 500
    page_size_query_param = "size"


class UserStationReadingsSensorsPagination(PageNumberPagination):
    page_size = 500
    page_size_query_param = "size"


class UserStationReadingsPagination(PageNumberPagination):
    page_size = 500
    page_size_query_param = "size"


class UserDataSetPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
