from rest_framework import serializers
from django.contrib.auth import get_user_model
from datadash.models import (
    StationStation,
    StationReadings,
    StationSensors,
    StationReadingsSensors,
)

CustomUser = get_user_model()


################################ UserSerializer #############################################


class UserStationReadingsSensorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationReadingsSensors
        fields = ["id", "data_value", "reading", "sensor"]


class UserStationSensorsSerializer(serializers.ModelSerializer):
    readings_sensors = serializers.SerializerMethodField()

    class Meta:
        model = StationSensors
        fields = ["id", "code", "name", "unit_measure", "readings_sensors"]

    def get_readings_sensors(self, obj):
        readings = self.context.get("readings")
        if readings:
            return UserStationReadingsSensorsSerializer(
                obj.sensors_readings.filter(reading__in=readings), many=True
            ).data
        return []


class UserStationReadingsSerializer(serializers.ModelSerializer):
    sensors = serializers.SerializerMethodField()

    class Meta:
        model = StationReadings
        fields = ["id", "time_measure", "sensors"]

    def get_sensors(self, obj):
        sensors = StationSensors.objects.filter(
            sensors_readings__reading=obj
        ).distinct()
        return UserStationSensorsSerializer(
            sensors, many=True, context={"readings": [obj]}
        ).data


class UserStationStationSerializer(serializers.ModelSerializer):
    readings = UserStationReadingsSerializer(many=True, read_only=True)

    class Meta:
        model = StationStation
        fields = ["id", "name", "location", "type", "user", "readings"]


############################### UserDataSetSerializers - Estrutura Aninhada #######################################


class StationReadingsSensorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationReadingsSensors
        fields = ["id", "data_value", "reading", "sensor"]


class StationSensorsSerializer(serializers.ModelSerializer):
    readings_sensors = serializers.SerializerMethodField()

    class Meta:
        model = StationSensors
        fields = ["id", "code", "name", "unit_measure", "readings_sensors"]

    def get_readings_sensors(self, obj):
        readings = self.context.get("readings")
        if readings:
            return StationReadingsSensorsSerializer(
                obj.sensors_readings.filter(reading__in=readings), many=True
            ).data
        return []


class StationReadingsSerializer(serializers.ModelSerializer):
    sensors = serializers.SerializerMethodField()

    class Meta:
        model = StationReadings
        fields = ["id", "time_measure", "sensors"]

    def get_sensors(self, obj):
        sensors = StationSensors.objects.filter(
            sensors_readings__reading=obj
        ).distinct()
        return StationSensorsSerializer(
            sensors, many=True, context={"readings": [obj]}
        ).data


class StationStationSerializer(serializers.ModelSerializer):
    readings = StationReadingsSerializer(many=True, read_only=True)

    class Meta:
        model = StationStation
        fields = ["id", "name", "location", "type", "user", "readings"]


class CustomUserSerializer(serializers.ModelSerializer):
    stations = StationStationSerializer(
        many=True, read_only=True, source="stationstation_set"
    )
    user = serializers.EmailField(source="email")

    class Meta:
        model = CustomUser
        fields = ["id", "user", "stations"]


class DataSetSerializer(serializers.Serializer):
    data_set = CustomUserSerializer(many=True)
