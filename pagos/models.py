from django.db import models
from Empresa.models import Empresa
from Login.models import Cuenta

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