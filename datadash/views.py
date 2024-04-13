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

    # class CustomViewSet(viewsets.ViewSet):

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


class CustomViewSet(viewsets.ViewSet):

    ##############################
    def criar_url(self, query_dict):  # AQUI FOI MUDADO
        query_dict_copy = (
            query_dict.copy()
        )  # AQUI CRIEI A COPIA, DEPOIS REFERENCIEI TUDO COMO query_dict_copy
        # Trata os valores no dicionário para remover '\r' e '\n'
        for chave, valor in query_dict_copy.items():
            query_dict_copy[chave] = [
                v.replace("\r", "").replace("\n", "") for v in valor
            ]

        # Substitui a primeira chave '!BDBSD' por 'cmd' e obtém o valor correspondente
        if "!BDBSD" in query_dict_copy:
            cmd = query_dict_copy.pop("!BDBSD")[0]
            # Adiciona ':' ao final do valor correspondente à primeira chave
            cmd += ":"
        else:
            cmd = None

        # Inicializa uma lista para armazenar os pares chave-valor
        pares = []

        # Itera sobre as chaves e valores do dicionário
        for chave, valor in query_dict_copy.items():
            # Adiciona o par chave-valor à lista de pares
            pares.append(f"{chave}={valor[0]}")

        # Concatena os pares usando vírgulas para formar o caminho da URL
        caminho = ",".join(pares)

        # Constrói a URL completa
        if cmd:
            url_completa = (
                f"http://recepcao.dualbase.com.br/recep/recep.php?cmd={cmd}{caminho}"
            )
        else:
            url_completa = f"http://recepcao.dualbase.com.br/recep/recep.php?{caminho}"

        # Concatena a string "895506:VTransDBv2.4:0" ao final da URL completa
        url_completa += ":895506:VTransDBv2.4:0"

        print(url_completa)

        return url_completa

    ##############################################
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

    ##############################
    def create(self, request):
        dados = request.data
        station_name = dados.get(
            "!BDBSD"
        )  # Obtém o nome da estação dos dados recebidos

        print("*******Dados**************")
        url = self.criar_url(dados)  # AQUI FOI MUDADO REFERENCIANDO SELF
        print(dados)
        print("*******Fim Dados**************")

        if station_name:
            try:
                # Busca a instância de StationStation com base no nome fornecido
                station_instance = StationStation.objects.get(name=station_name)
                station_reading_time_measure = dados.get(
                    "data"
                )  # RECEBE da estacao a data que o dado foi lido

                # print("**********************")
                print(station_reading_time_measure)
                # print("************************")

                # Separando a string em partes usando "_" como delimitador
                data, tempo = station_reading_time_measure.split("_")

                # Separando a parte da data em dia, mês e ano usando "-" como delimitador
                dia, mes, ano = map(int, data.split("-"))

                # Separando a parte da hora em hora e minuto usando "_" como delimitador
                hora, minuto = map(int, tempo.split("-"))

                # Dividindo a string em partes
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
