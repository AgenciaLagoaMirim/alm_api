from rest_framework.pagination import PageNumberPagination


class StationReadingsSensorsPagination(PageNumberPagination):
    page_size = 500
    page_size_query_param = "size"


class StationReadingsPagination(PageNumberPagination):
    page_size = 500
    page_size_query_param = "size"
