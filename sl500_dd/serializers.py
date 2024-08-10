from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Sl500, Sl500P


class Sl500PSerializer(ModelSerializer):
    cell_data = SerializerMethodField()

    class Meta:
        model = Sl500P
        fields = ["id", "cell_data"]

    def get_cell_data(self, obj):
        column_names = [
            "Id",
            "Parcial Id",
            "Cell",
            "Vx (cm/s)",
            "Errx(cms/s)",
            "Erry (cm/s)",
            "Amp1 (counts)",
            "Amp2 (counts)",
        ]

        data_values = [
            obj.id,
            obj.principal.id,
            obj.dado_0,
            obj.dado_1,
            obj.dado_2,
            obj.dado_3,
            obj.dado_4,
            obj.dado_5,
            obj.dado_6,
        ]

        sl500_data_set = dict(zip(column_names, data_values))

        return sl500_data_set





