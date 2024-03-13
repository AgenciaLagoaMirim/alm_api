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


class StationStationModelViewSet(viewsets.ModelViewSet):
    queryset = StationStation.objects.all()
    serializer_class = StationStationSerializer


class StationReadingsModelViewSet(viewsets.ModelViewSet):
    queryset = StationReadings.objects.all()
    serializer_class = StationReadingsSerializer


class CustomViewSet(viewsets.ViewSet):
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

                # JAMILSON !!!!
                # Aqui inicia a parte que temos que pegar na model o 'code'
                # Então, testar se na string de envio ex:
                #
                #
                # curl -X POST  http://185.137.92.73:8080/recebe/custom/ -d '!BDBSD=UFP_03&data=8-3-2024_10_5&TA_MIN=14&TA_AVG=21&TA_MAX=32&VB=12.3&TW=112'
                #
                #
                # veio alguma chave que corresponde. No exemplo do curl tem as chaves TA_MIN, TA_AVG, ...VB, TW
                # Então, pegamos o id. O id será usado para gravar  na model sensor_id.
                # Usaremos no reading_id o id da instancia de station_instance

                # Lista para armazenar os IDs dos sensores encontrados
                sensor_ids = []

                # Itera sobre os dados para encontrar correspondências com a model StationSensors
                # for key, value in dados.items():
                for key in dados.items():
                    # Verifica se o campo corresponde ao código ou nome do sensor
                    print(
                        key[0]
                    )  # em key[1] está o valor. É necessário depois instanciar a ultima model
                    # StationReadingsSensors será instanciada reading_id será igual para todos os sensores na leitura,
                    #  sensor_id e o data_value = key[1]
                    # if key in ['code', 'name']:
                    if key in ["code"]:
                        # Tenta encontrar a instância de StationSensors com base no código ou nome fornecido
                        try:
                            # sensor_instance = StationSensors.objects.get(station=station_instance, **{key: value})
                            sensor_instance = StationSensors.objects.get(
                                station=station_instance, code__iexact=key
                            )
                            print(
                                sensor_instance
                            )  # No servidor eu vejo os dados, mas não consigo instanciar aqui
                            sensor_ids.append(sensor_instance.id)
                        except StationSensors.DoesNotExist:
                            print(f"Sensor não encontrado para a chave '{key}'")
                            pass  # Lidar com o caso em que o sensor não é encontrado

                # Verifica se algum sensor foi encontrado
                if sensor_ids:
                    return Response(sensor_ids)
                else:
                    return Response(
                        {"message": "Nenhum sensor encontrado"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

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
