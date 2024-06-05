from django.contrib import admin
from .models import (
    StationStation,
    StationReadings,
    StationReadingsSensors,
    StationSensors,
)

admin.site.register(StationStation)
admin.site.register(StationReadings)
admin.site.register(StationReadingsSensors)
admin.site.register(StationSensors)
