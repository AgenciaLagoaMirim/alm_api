from rest_framework import routers

from .views import (
    CustomViewSet,
    StationReadingsModelViewSet,
    StationReadingsSensorsModelViewSet,
    StationStationModelViewSet,
    StationSensorsModelViewSet,
    UserStationStationViewSet,
    UserStationReadingsViewSet,
    UserStationSensorsViewSet,
    UserStationReadingsSensorsViewSet,
    UserDataSetViewSet,
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

data_dash_router.register(
    "user-station-stations", UserStationStationViewSet, basename="user-station-stations"
)

data_dash_router.register(
    "user-station-readings",
    UserStationReadingsViewSet,
    basename="user-station-readings",
)

data_dash_router.register(
    "user-station-sensors", UserStationSensorsViewSet, basename="user-station-sensors"
)

data_dash_router.register(
    "user-station-readings-sensors",
    UserStationReadingsSensorsViewSet,
    basename="user-station-reading-sensors",
)

data_dash_router.register("user-data-set", UserDataSetViewSet, basename="user-data-set")
