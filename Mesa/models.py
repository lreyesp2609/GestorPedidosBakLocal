from django.db import models
from Administrador.models import Administrador
from Cliente.models import Clientes

class Mesas(models.Model):
    ESTADO_CHOICES = [('D', 'D'), ('R', 'R'), ('U', 'U'), ('A', 'A')]
    ACTIVA_CHOICES = [('0', '0'), ('1', '1')]

    id_mesa = models.AutoField(primary_key=True)
    id_administrador = models.ForeignKey(Administrador, on_delete=models.CASCADE,db_column='id_administrador')
    observacion = models.CharField(max_length=500, null=True, blank=True)
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES, default='D')
    activa = models.CharField(max_length=1, choices=ACTIVA_CHOICES, default='0')
    maxpersonas = models.SmallIntegerField()
    sestado = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'mesas'



class Reservaciones(models.Model):
    ESTADO_CHOICES = [('E', 'E'), ('D', 'D'), ('F', 'F')]

    id_reservacion = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, db_column='id_cliente')
    id_mesa = models.ForeignKey(Mesas, on_delete=models.CASCADE, db_column='id_mesa')
    fecha_reserva = models.DateField()
    hora_reserva = models.TimeField()
    estado = models.CharField(max_length=1, choices=ESTADO_CHOICES)

    class Meta:
        managed = False
        db_table = 'reservaciones'