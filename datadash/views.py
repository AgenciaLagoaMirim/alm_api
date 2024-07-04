from .pagination import UserDataSetPagination
from .serializers import DataSetSerializer
from .models import CustomUser
from rest_framework import viewsets
from datetime import datetime
import requests
from django.http import HttpResponse

from rest_framework import status, viewsets
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .pagination import (
    StationReadingsPagination,
    StationReadingsSensorsPagination,
    UserStationReadingsPagination,
    UserStationReadingsSensorsPagination,
    UserDataSetPagination,
)
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

from .permissions import IsInGroupGeneralOrReadyOnly


# class StationReadingsSensorsModelViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = StationReadingsSensors.objects.all()
#     serializer_class = StationReadingsSensorsSerializer
#     pagination_class = StationReadingsSensorsPagination


# class StationReadingsModelViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = StationReadings.objects.all()
#     serializer_class = StationReadingsSerializer
#     pagination_class = StationReadingsPagination


# class StationSensorsModelViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = StationSensors.objects.all()
#     serializer_class = StationSensorsSerializer


# class StationStationModelViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = StationStation.objects.all()
#     serializer_class = StationStationSerializer


class CustomViewSet(viewsets.ViewSet):

    # DUAL BASE -
    def dualBase_url_via_get(self, url):
        print("------------------------------------------")
        print(url)
        print("------------------------------------------")
        try:
            # Faz a requisição GET para a URL fornecida
            response = requests.get(url)

            # Verifica se a requisição foi bem sucedida (código de status 200)
            if response.status_code == 200:
                return HttpResponse(f"A URL {url} foi chamada via GET com sucesso.")
            else:
                return HttpResponse(
                    f"A chamada para a URL {url} falhou com o código de status: {response.status_code}."
                )
        except requests.exceptions.RequestException as e:
            return HttpResponse(f"Erro ao chamar a URL {url}: {e}")

    ##############################################

    #
    # Altera dos dados POST para
    # http://recepcao.dualbase.com.br/recep/recep.php?cmd=UFP_03:data=7-4-2024_9-00,TA_AVG=nan,TA_MIN=nan,TA_MAX=nan,XR_AVG=0,XR_MIN=0,XR_MAX=0,PA_AVG=1011.77,PA_MIN=1011.58,PA_MAX=1012.06,US=0.264861,UD=162.854,PP=0,HG_AVG=nan,HG_MIN=nan,HG_MAX=nan,HG_02_AVG=nan,HG_02_MIN=nan,HG_02_MAX=nan,TW=0,VB=14.1410:89550680247000764359:VTransDBv2.4:0
    #

    def criar_url(self, query_dict):  # AQUI FOI MUDADO
        query_dict_copy = (
            query_dict.copy()
        )  # AQUI CRIEI A COPIA, DEPOIS REFERENCIEI TUDO COMO query_dict_copy
        # Trata os valores no dicionário para remover '\r' e '\n'
        for chave, valor in query_dict_copy.items():
            query_dict_copy[chave] = [
                v.replace("\r", "").replace("\n", "") for v in valor
            ]

        # print(query_dict_copy)
        # Inicializa um dicionário para armazenar as chaves e valores concatenados
        concatenado = {}

        # Iterando sobre as chaves e valores da QueryDict
        for chave, valor in query_dict_copy.items():
            # Verifica se a chave já está no dicionário de valores concatenados
            if chave in concatenado:
                # Se sim, concatena o valor atual com o valor existente
                concatenado[chave] += f",{'', join(valor)}"
            else:
                # Se não, adiciona o valor atual como uma nova entrada no dicionário
                concatenado[chave] = f"{''.join(valor)}"

        # Imprimindo as chaves e valores concatenados
        dados = ""
        for chave, valor in concatenado.items():
            # print(f"{chave}={valor},")
            dados += f"{chave}={valor},"
        dados = dados.rstrip(",")

        # Substituindo a ocorrência de !BDBSD por !BDBSD:
        # dualBaseSTR = dados.replace(("!BDBSD=", "?cmd="),("data=",":data="))
        dualBaseSTR_01 = dados.replace("!BDBSD=", "?cmd=")
        dualBaseSTR = dualBaseSTR_01.replace("data=", ":data=")
        partes = dualBaseSTR.split(",", 1)

        junta = partes[0] + partes[1]

        servidor_DualBase = "http://recepcao.dualbase.com.br/recep/recep.php"
        footer_DualBase = ":89550680247000764359:VTransDBv2.4:0"

        retorno = servidor_DualBase + junta + footer_DualBase

        #
        # ********
        # Se descomentar o print, e possível verificar que a url esta formada corretamente. Porém a chamada dessa função não está correta error 500 e 405
        # Possivel causa do erro 405
        #
        # https://apidog.com/blog/http-status-code-405/?utm_source=google_dsa&utm_medium=g&utm_campaign=21170664608&utm_content=166472884688&utm_term=&gad_source=1&gclid=CjwKCAjw_e2wBhAEEiwAyFFFo1yutYT1QBEc9hNIZCreJKu3TsSX-zIqvq8E7QP_uXILTIZ2-B_ugxoCRYUQAvD_BwE

        # print (retorno)

        return retorno

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
        print(station_name)
        print("*******Dados**************")
        # print(dados)
        print("*******Dados fim!**************")
        # station_save = StationStation.objects.get(name=station_name)
        # print(f"TESTE {station_save}")
        # station_type = station_save.get("type")
        # print(f"STATION TYPE {station_type}")

        # print(dualBase_url_via_get(url))
        # print(criar_url(url))
        # print(criar_url(url))
        print("*******Fim Dados**************")

        if station_name:
            try:
                # Busca a instância de StationStation com base no nome fornecido
                station_instance = StationStation.objects.get(name=station_name)
                station_reading_time_measure = dados.get(
                    "data"
                )  # RECEBE da estacao a data que o dado foi lido
                station_instance_type = station_instance.type
                print(f"TESTE {station_instance_type}")

                # TRATA RECEBIMENTO DOS EQUIPAMENTOS DE ACORD0 COM O TIPO
                if station_instance_type == "3":
                    url = self.criar_url(dados)  # AQUI FOI MUDADO REFERENCIANDO SELF
                    print(url)
                    self.dualBase_url_via_get(url)
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
                try:
                    # Salva a instância de StationReadings no banco de dados
                    station_reading.save()

                    # curl -X POST  http://185.137.92.73:8080/recebe/custom/ -d '!BDBSD=UFP_03&data=8-3-2024_10_5&TA_MIN=14&TA_AVG=21&TA_MAX=32&VB=12.3&TW=112'

                    # print(dados)

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

                            station_reading_sensor = (
                                StationReadingsSensors.objects.create(
                                    reading=station_reading,
                                    sensor=station_sensor,
                                    data_value=valor,
                                )
                            )

                    return Response(data_hora_formatada)

                except IntegrityError:
                    print("Esta leitura da estação já existe no banco de dados.")
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

    # class UserStationStationViewSet(viewsets.ModelViewSet):
    serializer_class = StationStationSerializer

    def get_queryset(self):
        """
        Retorna uma lista com todas as estações
        associadas ao usuário logado
        """
        user = self.request.user

        return StationStation.objects.filter(user=user.id)

    # class UserStationReadingsViewSet(viewsets.ModelViewSet):
    serializer_class = StationReadingsSerializer
    pagination_class = UserStationReadingsPagination

    def get_queryset(self):
        """
        Retorna uma lista com todas as  leituras das estações associadas ao
        usuário logado.
        """
        user_stations = StationStation.objects.filter(user=self.request.user)
        return StationReadings.objects.filter(station__in=user_stations)

    # class UserStationSensorsViewSet(viewsets.ModelViewSet):
    serializer_class = StationSensorsSerializer

    def get_queryset(self):
        """
        Retorna uma lista com todas as sensores associadas as
        estações do usuário logado.
        """
        user_stations = StationStation.objects.filter(user=self.request.user)
        return StationSensors.objects.filter(station__in=user_stations)

    # class UserStationReadingsSensorsViewSet(viewsets.ModelViewSet):
    serializer_class = StationReadingsSensorsSerializer

    def get_queryset(self):
        user_stations = StationStation.objects.filter(user=self.request.user)
        user_station_readings = StationReadings.objects.filter(
            station__in=user_stations
        )
        user_sensors_readings = StationSensors.objects.filter(station__in=user_stations)

        return StationReadingsSensors.objects.filter(
            reading__in=user_station_readings, sensor__in=user_sensors_readings
        )


class GeneralStationStationView(viewsets.ViewSet):
    queryset = StationStation.objects.all()
    serializer_class = StationSensorsSerializer
    permission_classes = [IsAuthenticated, IsInGroupGeneralOrReadyOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return StationReadings.objects.all()
        else:
            return StationStation.objects.filter(groups__name="general")

        return Response({"data_set": serialized_users.data})


CustomUser = get_user_model()


class UserDataSetViewSet(viewsets.ViewSet):
    pagination_class = UserDataSetPagination

    def list(self, request):
        paginator = UserDataSetPagination()
        user_objects = (
            CustomUser.objects.all()
            .order_by("id")
            .prefetch_related(
                "stations__readings__readings_sensors__sensor",
                "stations__sensors__station_sensors__reading",
            )
        )
        # "stations__readings__readings_sensors",
        # "stations__sensors__sensors_readings",
        user_page = paginator.paginate_queryset(user_objects, request)

        # Serializa os dados corretamente
        data_set_serializer = DataSetSerializer({"data_set": user_page})

        # Envolve a resposta paginada
        response_data = data_set_serializer.data
        return paginator.get_paginated_response(response_data)
