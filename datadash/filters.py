from django_filters import rest_framework as filters
from .models import StationStation


class StationStationFilter(filters.FilterSet):
    time_measure = filters.DateTimeFromToRangeFilter(
        field_name="readings__time_measure"
    )

    class Meta:
        model = StationStation
        fields = ["time_measure"]
