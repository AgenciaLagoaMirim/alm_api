from rest_framework import routers

from .views import (
    CustomViewSet,
    StationReadingsModelViewSet,
    StationReadingsSensorsModelViewSet,
    StationStationModelViewSet,
    StationSensorsModelViewSet,
)

data_dash_router = routers.DefaultRouter()
data_dash_router.register(
    "station-readings", StationReadingsModelViewSet, basename="station-readings"
)
data_dash_router.register(
    "station-readings-sensors",
    StationReadingsSensorsModelViewSet,
    basename="station-readings-sensors",
)
data_dash_router.register(
    "station-station", StationStationModelViewSet, basename="station-station"
)
data_dash_router.register(
    "station-sensors", StationSensorsModelViewSet, basename="station-sensors"
)
data_dash_router.register("custom-viewset", CustomViewSet, basename="custom-viewset")
