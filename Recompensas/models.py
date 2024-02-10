from django.db import models
from Combos.models import Combo
from Producto.models import Producto

class RecompensasProductos(models.Model):
    id_recompensaproducto = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto')
    puntos_recompensa_producto = models.DecimalField(max_digits=3, decimal_places=0)
    sestado = models.CharField(max_length=1, choices=[('0', '0'), ('1', '1')])

    class Meta:
        managed = False
        db_table = 'recompensasproductos'

class RecompensasCombos(models.Model):
    id_recompensacombo = models.AutoField(primary_key=True)
    id_combo = models.ForeignKey(Combo, on_delete=models.CASCADE, db_column='id_combo')
    puntos_recompensa_combo = models.DecimalField(max_digits=3, decimal_places=0)
    sestado = models.CharField(max_length=1, choices=[('0', '0'), ('1', '1')])

    class Meta:
        managed = False
        db_table = 'recompensascombos'