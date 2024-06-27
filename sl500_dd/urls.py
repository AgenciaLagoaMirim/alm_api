from rest_framework import routers

from .views import (
    Sl500DdViewSet,
    Sl500PDdViewSet,
    Sl500DataSetViewSet,
    DataReceptionSL500,
)

sl500_dd_router = routers.DefaultRouter()

sl500_dd_router.register("sl500-dd", Sl500DdViewSet, basename="sl500-dd")
sl500_dd_router.register("sl500p-dd", Sl500PDdViewSet, basename="sl500p-dd")
sl500_dd_router.register(
    "sl500-data-set", Sl500DataSetViewSet, basename="sl500p-data-set"
)
sl500_dd_router.register("sl500-dd-POST", DataReceptionSL500, basename="sl500-dd-POST")
