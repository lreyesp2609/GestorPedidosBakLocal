from django.db import models
from Empresa.models import Empresa
from Login.models import Cuenta
from Mesero.models import Pedidos

class Tipopago(models.Model):
    id_tipopago = models.AutoField(primary_key=True)
    idempresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, db_column='idempresa')
    rol = models.CharField(max_length=1, choices=[('X', 'X'), ('M', 'M'), ('D', 'D')], null=False)
    tipo_pago = models.CharField(max_length=1, choices=[('H', 'H'), ('S', 'S'), ('T', 'T'), ('M', 'M')], null=False, db_column='tipopago')
    cantidad = models.DecimalField(max_digits=8, decimal_places=2, null=False)

    class Meta:
        managed = False
        db_table = 'tipopago'

class Periodo(models.Model):
    id_periodo = models.AutoField(primary_key=True)
    rol = models.CharField(max_length=1, choices=[('X', 'X'), ('M', 'M'), ('D', 'D')], null=False)
    desde = models.DateTimeField(null=False)
    hasta = models.DateTimeField(null=False)

    class Meta:
        managed = False
        db_table = 'periodo'

class Pagos(models.Model):
    id_pago = models.AutoField(primary_key=True)
    idempleado = models.ForeignKey(Cuenta, on_delete=models.CASCADE, db_column='idempleado')
    cantidad = models.DecimalField(max_digits=8, decimal_places=2, null=False)
    tipopago = models.CharField(max_length=1, choices=[('H', 'H'), ('S', 'S'), ('T', 'T'), ('M', 'M')], null=False)
    idperiodo = models.ForeignKey(Periodo, on_delete=models.CASCADE, db_column='idperiodo')
    horadepago = models.DateTimeField(null=False)

    class Meta:
        managed = False
        db_table = 'pagos'
class PagosTransferencia(models.Model):
    id_pagotransferencia = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, db_column='id_pedido')
    estado = models.CharField(max_length=1, choices=[('E', 'E'), ('C', 'C')], null=False)
    cantidad = models.DecimalField(max_digits=9, decimal_places=2, null=False)
    hora_de_pago = models.DateTimeField(null=False)
    id_cuentacobrador = models.ForeignKey(Cuenta, on_delete=models.CASCADE, db_column='id_cuentacobrador')
    comprobante = models.BinaryField(null=False)
    hora_confirmacion_pago = models.DateTimeField(null=True)

    class Meta:
        managed = False
        db_table = 'pagostransferencia'
class PagosEfectivo(models.Model):
    id_pagoefectivo = models.AutoField(primary_key=True)
    estado = models.CharField(max_length=1, choices=[('X', 'X'), ('P', 'P')], null=False)
    cantidad = models.DecimalField(max_digits=9, decimal_places=2, null=False)
    cantidadentregada = models.DecimalField(max_digits=9, decimal_places=2, null=False, db_column='cantidadentregada')
    cambioeentregado = models.DecimalField(max_digits=9, decimal_places=2, null=False, db_column='cambioeentregado')
    hora_de_pago = models.DateTimeField(null=False)
    id_cuentacobrador = models.ForeignKey(Cuenta, on_delete=models.CASCADE, db_column='id_cuentacobrador')
    id_pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, db_column='id_pedido')

    class Meta:
        managed = False
        db_table = 'pagosefectivo'
class PagosPasarela(models.Model):
    id_pagopasarela = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, db_column='id_pedido')
    estado = models.CharField(max_length=1, choices=[('E', 'E'), ('C', 'C')], null=False)
    cantidad = models.DecimalField(max_digits=9, decimal_places=2, null=False)
    hora_de_pago = models.DateTimeField(null=False)
    codigo_unico = models.IntegerField(null=True)  # Cambiado a BinaryField para almacenar BYTEA

    class Meta:
        managed = False
        db_table = 'pagospasarela'