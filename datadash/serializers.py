from rest_framework.serializers import ModelSerializer

from .models import (
    StationReadings,
    StationReadingsSensors,
    StationSensors,
    StationStation,
)


class StationStationSerializer(ModelSerializer):
    class Meta:
        model = StationStation
        fields = "__all__"


class StationReadingsSerializer(ModelSerializer):
    class Meta:
        model = StationReadings
        fields = "__all__"


class StationSensorsSerializer(ModelSerializer):
    class Meta:
        model = StationSensors
        fields = "__all__"


class StationReadingsSensorsSerializer(ModelSerializer):
    class Meta:
        model = StationReadingsSensors
        fields = "__all__"
