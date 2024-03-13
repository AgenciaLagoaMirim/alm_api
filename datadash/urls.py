from rest_framework import routers

from .views import (
    CustomViewSet,
    StationReadingsModelViewSet,
    StationReadingsSensorsModelViewSet,
    StationStationModelViewSet,
)

data_dash_router = routers.DefaultRouter()
data_dash_router.register("station-readings", StationReadingsModelViewSet)
data_dash_router.register("station-readings-sensors", StationReadingsModelViewSet)
data_dash_router.register("station-station", StationReadingsModelViewSet)
data_dash_router.register("custom-viewset", CustomViewSet, basename="custom-viewset")
