from rest_framework import viewsets
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


class Sl500DataSetViewSet(viewsets.ViewSet):
    pagination_class = SL500DdPagination

    def list(self, request, *args, **kwargs):
        paginator = SL500DdPagination()

        sl500_objects = Sl500.objects.all()
        sl500_page = paginator.paginate_queryset(sl500_objects, request)
        sl500_serializer = Sl500Serializer(sl500_page, many=True)

        sl500p_objects = Sl500P.objects.all()
        sl500p_page = paginator.paginate_queryset(sl500p_objects, request)
        sl500p_serializer = Sl500PSerializer(sl500p_page, many=True)

        response_data = {
            "sl500": sl500_serializer.data,
            "sl500p": sl500p_serializer.data,
        }

        return paginator.get_paginated_response(response_data)
