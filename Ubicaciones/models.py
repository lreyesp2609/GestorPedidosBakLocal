from django.db import models

# Create your models here.
class Ubicaciones(models.Model):
    id_ubicacion = models.AutoField(primary_key=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    udescripcion = models.CharField(max_length=500, blank=True, null=True)
    sestado = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'ubicaciones'