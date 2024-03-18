from datetime import datetime

from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from .models import (
    StationReadings,
    StationReadingsSensors,
    StationSensors,
    StationStation,
)
from .serializers import (
    StationReadingsSensorsSerializer,
    StationReadingsSerializer,
    StationSensorsSerializer,
    StationStationSerializer,
)


class StationReadingsSensorsModelViewSet(viewsets.ModelViewSet):
    queryset = StationReadingsSensors.objects.all()
    serializer_class = StationReadingsSensorsSerializer


class StationReadingsModelViewSet(viewsets.ModelViewSet):
    queryset = StationReadings.objects.all()
    serializer_class = StationReadingsSerializer


class StationSensorsModelViewSet(viewsets.ModelViewSet):
    queryset = StationSensors.objects.all()
    serializer_class = StationSensorsSerializer


class StationStationModelViewSet(viewsets.ModelViewSet):
    queryset = StationStation.objects.all()
    serializer_class = StationStationSerializer


class CustomViewSet(viewsets.ViewSet):

    def can_be_stored_as_double(self, value):
        try:
            # Tenta converter o valor para float
            float_value = float(value)
            # Verifica se o valor está dentro da faixa de valores suportada pelo tipo double no PostgreSQL
            if -1.7976931348623157e308 <= float_value <= 1.7976931348623157e308:
                return True
            else:
                return False
        except ValueError:
            # Se a conversão para float falhar, significa que o valor não pode ser armazenado como double
            return False

    def create(self, request):
        dados = request.data
        station_name = dados.get(
            "!BDBSD"
        )  # Obtém o nome da estação dos dados recebidos
        if station_name:
            try:
                # Busca a instância de StationStation com base no nome fornecido
                station_instance = StationStation.objects.get(name=station_name)
                station_reading_time_measure = dados.get(
                    "data"
                )  # RECEBE da estacao a data que o dado foi lido
                # Dividindo a string em partes
                data_hora_parts = station_reading_time_measure.split("_")
                # Obtendo as partes da data
                dia, mes, ano = map(int, data_hora_parts[0].split("-"))
                # Obtendo as partes da hora
                hora, minuto = map(int, data_hora_parts[1:])
                # Criando um objeto datetime
                data_hora = datetime(ano, mes, dia, hora, minuto)
                # Formatando a data e hora conforme desejado
                data_hora_formatada = data_hora.strftime("%Y-%m-%d %H:%M")

                # Cria uma nova instância de StationReadings associada à instância de StationStation encontrada
                station_reading = StationReadings(
                    station=station_instance, time_measure=data_hora_formatada
                )
                # Salva a instância de StationReadings no banco de dados
                station_reading.save()
                # curl -X POST  http://185.137.92.73:8080/recebe/custom/ -d '!BDBSD=UFP_03&data=8-3-2024_10_5&TA_MIN=14&TA_AVG=21&TA_MAX=32&VB=12.3&TW=112'
                print(dados)
                # for i in dados.items():
                #   print(f"var = {i[1]}")
                for indice, (chave, valor) in enumerate(dados.items()):
                    if indice > 1:
                        print(f"Chave: {chave}, Valor: {valor}")
                        if self.can_be_stored_as_double(valor):
                            valor = valor
                        else:
                            valor = None
                        station_sensor = StationSensors.objects.get(
                            code=chave, station=station_instance
                        )

                        station_reading_sensor = StationReadingsSensors.objects.create(
                            reading=station_reading,
                            sensor=station_sensor,
                            data_value=valor,
                        )
                return Response(data_hora_formatada)

            except StationStation.DoesNotExist:
                return Response(
                    {"message": "Estação não encontrada"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            return Response(
                {"message": "Nome da estação não fornecido"},
                status=status.HTTP_400_BAD_REQUEST,
            )
