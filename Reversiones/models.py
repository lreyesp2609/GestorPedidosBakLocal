from django.db import models
from Cliente.models import Clientes
from Mesero.models import Pedidos


class Cuenta(models.Model):
    id_cuenta = models.AutoField(primary_key=True)
    nombreusuario = models.CharField(max_length=300)
    contrasenia = models.CharField()
    fechacreacion = models.DateTimeField(auto_now_add=True)
    fechafin = models.DateTimeField(null=True, blank=True)
    observacion = models.CharField(max_length=500, null=True, blank=True)
    fotoperfil = models.BinaryField(null=True, blank=True)
    estadocuenta = models.CharField(max_length=1, choices=[('0', '0'), ('1', '1')])
    rol = models.CharField(max_length=1, choices=[('A', 'A'), ('C', 'C'), ('X', 'X'), ('M', 'M'), ('D', 'D'),('S', 'S')])
    correorecuperacion = models.CharField(max_length=256, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'cuenta'

class ReversionPedidos(models.Model):
    id_reversion = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE, db_column='id_pedido')
    id_cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, db_column='id_cuenta')
    fecha_cancelacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'reversionpedidos'
