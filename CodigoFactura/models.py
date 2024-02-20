from datetime import datetime, timezone
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from Administrador.models import *
# Create your models here.

class Codigosri(models.Model):
    id_codigosri = models.AutoField(primary_key=True)
    id_administrador = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='id_administrador', blank=True, null=True)
    numero_factura_desde = models.CharField(max_length=9)  # Este será el primer número de factura en el rango
    numero_factura_hasta = models.CharField(max_length=9)  # Este será el último número de factura en el rango
    rango_desde = models.CharField(max_length=9)  # Este será el próximo número de factura a usar
    rango_hasta = models.CharField(max_length=9)  # Este será el último número de factura en el rango

    class Meta:
        managed = False
        db_table = 'codigosri'
        unique_together = (('rango_desde', 'rango_hasta'),)

    @classmethod
    def obtener_proximo_numero_factura(cls, id_mesero, id_sucursal):
        try:
            codigosri = cls.objects.get()  # Suponiendo que solo hay un registro en Codigosri

            numero_actual = int(codigosri.rango_desde)
            numero_hasta = int(codigosri.rango_hasta)

            codigo_establecimiento = str(id_sucursal).zfill(3)

            if numero_actual <= numero_hasta:
                numero_formateado = f"{codigo_establecimiento}{str(id_mesero).zfill(3)}{str(numero_actual).zfill(9)}"
                codigosri.rango_desde = str(numero_actual + 1).zfill(9)
                codigosri.save()
                return numero_formateado, codigosri.numero_factura_desde, codigosri.numero_factura_hasta
            else:
                raise ValueError("No hay más números de factura disponibles")
        except ObjectDoesNotExist:
            raise ValueError("No se encontró ningún registro en Codigosri")

        
class Codigoautorizacion(models.Model):
    id_codigosauto = models.AutoField(primary_key=True)
    id_administrador = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='id_administrador', blank=True, null=True)
    codigo_autorizacion = models.CharField(max_length=10)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    fecha_autorizacion = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'codigoautorizacion'
    @classmethod
    def obtener_codigo_autorizacion_valido(cls):
        try:
            codigo_autorizacion = cls.objects.filter(fecha_vencimiento__gte=datetime.now(timezone.utc)).first()
            if codigo_autorizacion:
                codigo_autorizacion.fecha_autorizacion = datetime.now(timezone.utc)
                codigo_autorizacion.save()
                return codigo_autorizacion.codigo_autorizacion
            else:
                return None
        except ObjectDoesNotExist:
            return None