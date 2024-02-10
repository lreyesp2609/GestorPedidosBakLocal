from django.db import models
from Ubicaciones.models import Ubicaciones

# Create your models here.
class Geosectores(models.Model):
    id_geosector = models.AutoField(primary_key=True)
    fechacreaciong = models.DateTimeField()
    secnombre = models.CharField(max_length=300)
    secdescripcion = models.CharField(max_length=500, blank=True, null=True)
    sectipo = models.CharField(max_length=1)
    secestado = models.CharField(max_length=1)
    sestado = models.CharField(max_length=1)
    tarifa = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'geosectores'

class DetalleGeosector(models.Model):
    id_detallegeosector = models.AutoField(primary_key=True)
    id_geosector = models.ForeignKey(Geosectores, on_delete=models.CASCADE,db_column='id_geosector')
    id_ubicacion = models.ForeignKey(Ubicaciones, on_delete=models.CASCADE, db_column='id_ubicacion')

    class Meta:
        managed = False
        db_table = 'detalle_geosector'