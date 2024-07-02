from django.contrib.auth import get_user_model
from django.db import models

CustomUser = get_user_model()


class StationStation(models.Model):
    STATION_TYPE_CHOICES = (
        ("0", "Teste"),
        ("1", "Solar"),
        ("2", "SL500"),
        ("3", "DualBase"),
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(
        CustomUser, models.DO_NOTHING, blank=True, null=True, related_name="stations"
    )
    type = models.CharField(
        max_length=1, choices=STATION_TYPE_CHOICES, blank=False, null=False
    )

    class Meta:
        db_table = "station_station"


class StationReadings(models.Model):
    station = models.ForeignKey(
        StationStation,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="readings",
    )
    time_measure = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "station_readings"


class StationSensors(models.Model):
    station = models.ForeignKey(
        StationStation, models.DO_NOTHING, blank=True, null=True, related_name="sensors"
    )
    code = models.CharField(max_length=10, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    unit_measure = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = "station_sensors"


class StationReadingsSensors(models.Model):
    id = models.BigAutoField(primary_key=True)
    data_value = models.DecimalField(
        max_digits=10, decimal_places=3, blank=True, null=True
    )
    reading = models.ForeignKey(
        StationReadings,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="readings_sensors",
    )
    sensor = models.ForeignKey(
        StationSensors,
        models.DO_NOTHING,
        blank=True,
        null=True,
        related_name="readings_sensors",
    )

    class Meta:
        managed = False
        db_table = "station_readings_sensors"
