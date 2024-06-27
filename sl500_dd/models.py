from django.db import models
from datadash.models import StationStation


class Sl500(models.Model):
    id = models.BigIntegerField(primary_key=True)
    ano = models.IntegerField(blank=True, null=True)
    mes = models.IntegerField(blank=True, null=True)
    dia = models.IntegerField(blank=True, null=True)
    hora = models.IntegerField(blank=True, null=True)
    minuto = models.IntegerField(blank=True, null=True)
    segundo = models.IntegerField(blank=True, null=True)
    dado1 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dado2 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dado3 = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    dado4 = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    dado5 = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    dado6 = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    dado7 = models.IntegerField(blank=True, null=True)
    dado8 = models.IntegerField(blank=True, null=True)
    dado9 = models.IntegerField(blank=True, null=True)
    dado10 = models.IntegerField(blank=True, null=True)
    dado11 = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    dado12 = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    dado13 = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True)
    dado14 = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    dado15 = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    dado16 = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    dado17 = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    dado18 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dado19 = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    dado20 = models.DecimalField(max_digits=5, decimal_places=3, blank=True, null=True)
    dado21 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dado22 = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    dado23 = models.IntegerField(blank=True, null=True)
    dado24 = models.IntegerField(blank=True, null=True)
    dado25 = models.IntegerField(blank=True, null=True)
    data_safe = models.DateTimeField()
    local_date = models.DateTimeField()
    station = models.ForeignKey(
        StationStation, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        db_table = "sl500"


class Sl500P(models.Model):
    id = models.BigIntegerField(primary_key=True)
    principal = models.ForeignKey(Sl500, models.DO_NOTHING, related_name="sl500p_set")
    dado_0 = models.IntegerField()
    dado_1 = models.FloatField(blank=True, null=True)
    dado_2 = models.FloatField(blank=True, null=True)
    dado_3 = models.FloatField(blank=True, null=True)
    dado_4 = models.FloatField(blank=True, null=True)
    dado_5 = models.FloatField(blank=True, null=True)
    dado_6 = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = "sl500p"
