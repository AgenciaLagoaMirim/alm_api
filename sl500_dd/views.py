from rest_framework import viewsets
from rest_framework.response import Response
from .models import Sl500, Sl500P
from .serializers import Sl500Serializer, Sl500PSerializer
from .pagination import SL500DdPagination


class Sl500DdViewSet(viewsets.ModelViewSet):
    queryset = Sl500.objects.all()
    pagination_class = SL500DdPagination
    serializer_class = Sl500Serializer


class Sl500PDdViewSet(viewsets.ModelViewSet):
    queryset = Sl500P.objects.all()
    pagination_class = SL500DdPagination
    serializer_class = Sl500PSerializer


#  todo fazer outra baseada no usuário
class Sl500DataSetViewSet(viewsets.ViewSet):
    pagination_class = SL500DdPagination

    def list(self, request, *args, **kwargs):
        paginator = SL500DdPagination()
        sl500_objects = Sl500.objects.all()
        sl500_page = paginator.paginate_queryset(sl500_objects, request)
        sl500_serializer = Sl500Serializer(sl500_page, many=True)

        response_data = {"sl500_data_set": sl500_serializer.data}
        return paginator.get_paginated_response(response_data)
