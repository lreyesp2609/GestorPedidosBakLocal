from django.db import models

from Administrador.models import Administrador
from Cliente.models import Cuenta
from Mesero.models import Pedidos
from Sucursal.models import Sucursales

class Motorizados(models.Model):
    id_motorizado = models.AutoField(primary_key=True)
    id_sucursal = models.ForeignKey(Sucursales, models.DO_NOTHING, db_column='id_sucursal')
    id_administrador = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='id_administrador')
    nombre = models.CharField(max_length=300)
    apellido = models.CharField(max_length=300)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    fecha_registro = models.DateTimeField()
    id_cuenta = models.ForeignKey(Cuenta, models.DO_NOTHING, db_column='id_cuenta', blank=True, null=True)
    sestado = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'motorizados'

class PedidosMotorizado(models.Model):
    id_pedido_motorizado = models.AutoField(primary_key=True)
    id_motorizado = models.ForeignKey(Motorizados, models.DO_NOTHING, db_column='id_motorizado')
    id_pedido = models.ForeignKey(Pedidos, models.DO_NOTHING, db_column='id_pedido')
    cantidad = models.PositiveIntegerField(default=1)  # Cantidad de pedidos que el motorizado llevará
    fecha_aceptacion = models.DateTimeField(auto_now_add=True)  # Fecha en que el motorizado aceptó el pedido

    class Meta:
        managed = False
        db_table = 'pedidos_motorizado'

from django.db import models
from Motorizado.models import Motorizados

class CajaDiaria(models.Model):
    id_caja = models.AutoField(primary_key=True)
    id_motorizado = models.ForeignKey(Motorizados, models.DO_NOTHING, db_column='id_motorizado')
    fecha = models.DateField(auto_now_add=True)  # Fecha de la caja diaria
    monto_acumulado = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Monto acumulado

    class Meta:
        managed = False
        db_table = 'caja_diaria'