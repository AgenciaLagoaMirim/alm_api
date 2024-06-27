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


class Sl500Serializer(ModelSerializer):
    sl500_data = SerializerMethodField()
    cells_data_set = Sl500PSerializer(many=True, read_only=True, source="sl500p_set")

    class Meta:
        model = Sl500
        fields = ["id", "sl500_data", "cells_data_set"]

    def get_sl500_data(self, obj):
        column_names = [
            "Id",
            "Data",
            "VEL_X(cm/s)",
            "VEL_Y(cm/s)",
            "LEVEL(m)",
            "VelStDev1/X/E (cm/s)",
            "VelStDev2/Y/N (cm/s)",
            "VelStDev3/Z/U (cm/s)",
            "SignalAmp1 (counts)",
            "SignalAmp2 (counts)",
            "SignalAmp3 (counts)",
            "Ice Detection",
            "Heading (deg)",
            "Pitch (deg)",
            "Roll (deg)",
            "Standard deviation of the Heading (deg)",
            "Standard deviation of the Pitch (deg)",
            "Standard deviation of the Roll (deg)",
            "Mean Tempr (degC)",
            "MeanPress (dBar)",
            "StDevPress (dBar)",
            "Power level (battery voltage) (Volts)",
            "CellBegin (m)",
            "CellEnd (m)",
            "Noise 1",
            "Noise 2",
            "Noise 3",
            "Data Safe",
            "Local Date",
            "Station",
        ]
        data_values = [
            obj.id,
            obj.data_safe.isoformat(),
            obj.dado1,
            obj.dado2,
            obj.dado3,
            obj.dado4,
            obj.dado5,
            obj.dado6,
            obj.dado7,
            obj.dado8,
            obj.dado9,
            obj.dado10,
            obj.dado11,
            obj.dado12,
            obj.dado13,
            obj.dado14,
            obj.dado15,
            obj.dado16,
            obj.dado17,
            obj.dado18,
            obj.dado19,
            obj.dado20,
            obj.dado21,
            obj.dado22,
            obj.dado23,
            obj.dado24,
            obj.dado25,
            obj.data_safe.isoformat(),
            obj.local_date.isoformat(),
            obj.station.id if obj.station else None,
        ]

        # Mapeia os nomes das colunas para os dados
        sl500_data = dict(zip(column_names, data_values))

        return sl500_data
