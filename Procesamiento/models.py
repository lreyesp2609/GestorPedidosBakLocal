from django.db import models
from Administrador.models import Cuenta
from Bodega.models import Bodegas

class Procesamiento(models.Model):
    id_procesamientos = models.AutoField(primary_key=True)
    id_cuenta = models.ForeignKey(Cuenta, models.DO_NOTHING, db_column='id_cuenta')
    tipo_de_proceso = models.CharField(max_length=1)
    observacion = models.CharField(max_length=500, blank=True, null=True)
    fecha_de_procesamiento = models.DateTimeField()
    id_bodega = models.ForeignKey(Bodegas, models.DO_NOTHING, db_column='id_bodega')

    class Meta:
        managed = False
        db_table = 'procesamiento'