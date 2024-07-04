from rest_framework import serializers
from django.contrib.auth import get_user_model
from datadash.models import (
    StationStation,
    StationReadings,
    StationSensors,
    StationReadingsSensors,
)

CustomUser = get_user_model()


class StationReadingsSensorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationReadingsSensors
        fields = ["id", "data_value", "reading", "sensor"]


class StationSensorsSerializer(serializers.ModelSerializer):
    readings_sensors = StationReadingsSensorsSerializer(many=True, read_only=True)

    class Meta:
        model = StationSensors
        fields = ["id", "code", "name", "unit_measure", "station", "readings_sensors"]


class StationReadingsSerializer(serializers.ModelSerializer):
    sensors = serializers.SerializerMethodField()

    class Meta:
        model = StationReadings
        fields = ["id", "time_measure", "station", "sensors"]

    def get_sensors(self, obj):
        sensors = StationSensors.objects.filter(station=obj.station)
        return StationSensorsSerializer(sensors, many=True).data


class StationStationSerializer(serializers.ModelSerializer):
    readings = StationReadingsSerializer(many=True, read_only=True)

    class Meta:
        model = StationStation
        fields = ["id", "name", "location", "type", "user", "readings"]


class CustomUserSerializer(serializers.ModelSerializer):
    stations = StationStationSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "stations"]


class DataSetSerializer(serializers.Serializer):
    data_set = CustomUserSerializer(many=True)


class UserDataSetViewSet(viewsets.ViewSet):
    pagination_class = UserDataSetPagination

    def list(self, request):
        paginator = UserDataSetPagination()
        user_objects = (
            CustomUser.objects.all()
            .order_by("id")
            .prefetch_related(
                "stations__readings__readings_sensors__sensor",
                "stations__sensors__sensors_readings__reading",
            )
        )
        user_page = paginator.paginate_queryset(user_objects, request)

        # Serializa os dados corretamente
        data_set_serializer = DataSetSerializer({"data_set": user_page})

        # Envolve a resposta paginada
        response_data = data_set_serializer.data
        return paginator.get_paginated_response(response_data)
