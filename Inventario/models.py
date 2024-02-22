from django.db import models
from Producto.models import *
from Bodega.models import *
from django.utils import timezone
from Login.models import Cuenta
from Mesero.models import Pedidos
from Proveedores.models import Pedidosproveedor

class MovimientoInventario(models.Model):
    id_movimientoinventario = models.AutoField(primary_key=True)
    id_cuenta = models.ForeignKey(Cuenta, models.DO_NOTHING, db_column='id_cuenta')
    id_pedido = models.ForeignKey(Pedidos, models.DO_NOTHING, db_column='id_pedido', blank=True, null=True)
    id_pedidoproveedor = models.ForeignKey(Pedidosproveedor, models.DO_NOTHING, db_column='id_pedidoproveedor', blank=True, null=True)
    id_bodega = models.ForeignKey(Bodegas, models.DO_NOTHING, db_column='id_bodega', blank=True, null=True)
    fechahora = models.DateTimeField(default=timezone.now)
    tipomovimiento = models.CharField(max_length=1, choices=[('E', 'Entrada'), ('S', 'Salida'), ('P', 'Preparacion'), ('R', 'Reversion')])
    observacion = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'movimientoinventario'


class DetalleMovimientoInventario(models.Model):
    id_detallemovimiento = models.AutoField(primary_key=True)
    id_movimientoinventario = models.ForeignKey(MovimientoInventario, models.DO_NOTHING, db_column='id_movimientoinventario')
    id_articulo = models.ForeignKey(Componente, models.DO_NOTHING, db_column='id_articulo', blank=True, null=True)
    id_producto = models.ForeignKey(Producto, models.DO_NOTHING, db_column='id_producto', blank=True, null=True)
    cantidad = models.DecimalField(max_digits=9, decimal_places=2)
    tipo = models.CharField(max_length=1, choices=[('E', 'Entrada'), ('S', 'Salida')])
    
    class Meta:
        managed = False
        db_table = 'detallemovimientoinventario'

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

