from django.http import JsonResponse
from django.http import HttpResponse
import requests
from datetime import datetime
from .pagination import SL500DdPagination
from .serializers import Sl500Serializer, Sl500PSerializer
from .models import Sl500, Sl500P, StationStation
from .models import Sl500, Sl500P
from rest_framework.response import Response
from rest_framework import viewsets


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

        response_data = {"sl500_data_set": sl500_serializer.data}
        return paginator.get_paginated_response(response_data)


class DataReceptionSL500(viewsets.ViewSet):

    def process_data(self, raw_data):
        if "#" in raw_data:
            # Dividir a string pelo primeiro '#' para obter a primeira linha completa
            first_line, remaining_data = raw_data.split("#", 1)
            first_line = first_line.strip()

            # Dividir as linhas restantes pelo caractere '#'
            lines = remaining_data.split("#")
            lines = [line.strip() for line in lines if line.strip()]

            # Dividir a primeira linha em partes individuais
            first_line_parts = first_line.split()

            # Dividir cada linha de SL500P em partes individuais
            sl500p_data = []
            for line in lines:
                line_parts = line.split()
                if len(line_parts) >= 7:  # Garantir que haja pelo menos 7 partes em cada linha de SL500P
                    sl500p_data.append(line_parts)

            return {"SL500": first_line_parts, "SL500P": sl500p_data}
        else:
            return {"error": 'No "#" found in the data'}

    def create(self, request):
        raw_data = request.data.get("DADOS", "")
        station_name = request.data.get("st_name", None)

        processed_data = self.process_data(raw_data)

        if "error" in processed_data:
            return Response(processed_data, status=400)

        try:
            # Buscar a estação pelo nome
            station = StationStation.objects.filter(name=station_name).first()
            if not station:
                return Response({"error": "Station not found"}, status=404)

            # Salvando dados em Sl500
            sl500_data = processed_data["SL500"]
            sl500 = Sl500.objects.create(
                ano=int(sl500_data[0]),
                mes=int(sl500_data[1]),
                dia=int(sl500_data[2]),
                hora=int(sl500_data[3]),
                minuto=int(sl500_data[4]),
                segundo=float(sl500_data[5]),
                dado1=float(sl500_data[6]),
                dado2=float(sl500_data[7]),
                dado3=float(sl500_data[8]),
                dado4=float(sl500_data[9]),
                dado5=float(sl500_data[10]),
                dado6=float(sl500_data[11]),
                dado7=int(sl500_data[12]),
                dado8=int(sl500_data[13]),
                dado9=int(sl500_data[14]),
                dado10=int(sl500_data[15]),
                dado11=float(sl500_data[16]),
                dado12=float(sl500_data[17]),
                dado13=float(sl500_data[18]),
                dado14=float(sl500_data[19]),
                dado15=float(sl500_data[20]),
                dado16=float(sl500_data[21]),
                dado17=float(sl500_data[22]),
                dado18=float(sl500_data[23]),
                dado19=float(sl500_data[24]),
                dado20=float(sl500_data[25]),
                dado21=float(sl500_data[26]),
                dado22=float(sl500_data[27]),
                dado23=int(sl500_data[28]),
                dado24=int(sl500_data[29]),
                dado25=int(sl500_data[30]),
                data_safe=datetime.now(),
                local_date=datetime.now(),
                station=station,
            )

            # Salvando dados em Sl500P
            sl500p_data = processed_data["SL500P"]
            for line_parts in sl500p_data:
                print(f"Creating Sl500P: principal={sl500}, dado_0={line_parts[0]}, dado_1={line_parts[1]}, dado_2={line_parts[2]}, dado_3={line_parts[3]}, dado_4={line_parts[4]}, dado_5={line_parts[5]}, dado_6={line_parts[6]}")
                # Não definir o campo 'id', pois deve ser auto-incrementado
                Sl500P.objects.create(
                    principal=sl500,
                    dado_0=int(line_parts[0]),
                    dado_1=float(line_parts[1]),
                    dado_2=float(line_parts[2]),
                    dado_3=float(line_parts[3]),
                    dado_4=float(line_parts[4]),
                    dado_5=float(line_parts[5]),
                    dado_6=int(line_parts[6]),
                )

            return Response({"message": "Data saved successfully"}, status=201)

        except Exception as e:
            return Response({"error": str(e)}, status=500)