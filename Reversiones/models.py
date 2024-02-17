from django.db import models
from Inventario.models import MovimientoInventario
from Login.models import Cuenta

class ReversionMovimientoInventario(models.Model):
    id_reversion = models.AutoField(primary_key=True)
    id_movimientoinventario = models.ForeignKey(MovimientoInventario, on_delete=models.CASCADE, db_column='id_MovimientoInventario')
    id_cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, db_column='id_Cuenta')
    fechahora = models.DateTimeField(auto_now_add=True)
    motivo = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'reversionmovimientoinventario'

