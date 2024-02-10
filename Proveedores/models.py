from django.db import models
from Administrador.models import Administrador
from Bodega.models import Bodegas
from Producto.models import *

class Proveedores(models.Model):
    id_proveedor = models.AutoField(primary_key=True, db_column='id_proveedor')
    nombreproveedor = models.CharField(max_length=300, db_column='nombreproveedor')
    direccionproveedor = models.CharField(max_length=300, blank=True, null=True, db_column='direccionproveedor')
    telefonoproveedor = models.CharField(max_length=10, blank=True, null=True, db_column='telefonoproveedor')
    correoproveedor = models.CharField(max_length=256, blank=True, null=True, db_column='correoproveedor')
    id_administrador = models.ForeignKey(Administrador, on_delete=models.DO_NOTHING, db_column='id_administrador')
    sestado = models.CharField(max_length=1, choices=[('0', '0'), ('1', '1')], db_column='sestado')

    class Meta:
        managed = False
        db_table = 'proveedores'

class Pedidosproveedor(models.Model):
    id_pedidoproveedor = models.AutoField(primary_key=True)
    id_proveedor = models.ForeignKey(Proveedores, models.DO_NOTHING, db_column='id_proveedor')
    id_bodega = models.ForeignKey(Bodegas, models.DO_NOTHING, db_column='id_bodega')
    fechapedido = models.DateTimeField()
    fechaentregaesperada = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=1)
    observacion = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pedidosproveedor' 

class Detallepedidoproveedor(models.Model):
    id_detallepedidoproveedor = models.AutoField(primary_key=True)
    id_pedidoproveedor = models.ForeignKey(Pedidosproveedor, models.DO_NOTHING, db_column='id_pedidoproveedor')
    id_producto = models.ForeignKey(Producto, models.DO_NOTHING, db_column='id_producto', blank=True, null=True)
    id_componente = models.ForeignKey(Componente, models.DO_NOTHING, db_column='id_componente', blank=True, null=True)
    cantidad = models.DecimalField(max_digits=9, decimal_places=2)
    costounitario = models.DecimalField(max_digits=9, decimal_places=2)
    id_um = models.ForeignKey(UnidadMedida, models.DO_NOTHING, db_column='id_um', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detallepedidoproveedor'

