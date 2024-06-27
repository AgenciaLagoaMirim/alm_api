from rest_framework import serializers
from .models import (
    StationStation,
    StationReadings,
    StationSensors,
    StationReadingsSensors,
)
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class StationReadingsSensorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationReadingsSensors
        fields = ["id", "data_value", "reading", "sensor"]


class StationSensorsSerializer(serializers.ModelSerializer):
    readings_sensors = StationReadingsSensorsSerializer(
        many=True, read_only=True, source="station_readings"
    )

    class Meta:
        model = StationSensors
        fields = ["id", "code", "name", "unit_measure", "station", "readings_sensors"]


class StationReadingsSerializer(serializers.ModelSerializer):
    sensors = StationSensorsSerializer(many=True, read_only=True)

    class Meta:
        model = StationReadings
        fields = ["id", "time_measure", "station", "sensors"]


class StationStationSerializer(serializers.ModelSerializer):
    readings = StationReadingsSerializer(many=True, read_only=True)
    sensors = StationSensorsSerializer(many=True, read_only=True)

    class Meta:
        model = StationStation
        fields = ["id", "name", "location", "type", "user", "readings", "sensors"]


class CustomUserSerializer(serializers.ModelSerializer):
    stations = StationStationSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "stations"]
