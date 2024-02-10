from django.db import models
from Producto.models import *
from Bodega.models import *
# Create your models here.

class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    id_bodega = models.ForeignKey(Bodegas, models.DO_NOTHING, db_column='id_bodega')
    id_producto = models.ForeignKey(Producto, models.DO_NOTHING, db_column='id_producto', blank=True, null=True)
    id_componente = models.ForeignKey(Componente, models.DO_NOTHING, db_column='id_componente', blank=True, null=True)
    costo_unitario = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    id_um = models.ForeignKey(UnidadMedida, models.DO_NOTHING, db_column='id_um', blank=True, null=True)
    stock_minimo = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    cantidad_disponible = models.DecimalField(max_digits=9, decimal_places=2)
    class Meta:
        managed = False
        db_table = 'inventario'

