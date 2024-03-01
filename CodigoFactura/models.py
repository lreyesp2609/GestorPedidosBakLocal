from django.utils import timezone
from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from Administrador.models import *


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
    def obtener_proximo_numero_factura(cls, id_punto_facturacion, id_sucursal):
        try:
            punto_facturacion = Puntofacturacion.objects.get(id_puntofacturacion=id_punto_facturacion)
            if punto_facturacion:
                if punto_facturacion.id_administrador:
                    codigosri_instance = cls.objects.get()  # Guarda la instancia de Codigosri
                    numero_actual = int(codigosri_instance.rango_desde)
                    numero_hasta = int(codigosri_instance.rango_hasta)
                    codigo_punto_facturacion = punto_facturacion.codigo.zfill(3)

                    if numero_actual <= numero_hasta:
                        numero_formateado = f"{codigo_punto_facturacion}{str(numero_actual).zfill(9)}"
                        codigosri_instance.rango_desde = str(numero_actual + 1).zfill(9)
                        codigosri_instance.save()  # Guarda la instancia actualizada
                        return numero_formateado, codigosri_instance.numero_factura_desde, codigosri_instance.numero_factura_hasta
                    else:
                        raise ValueError("No hay más números de factura disponibles")
                else:
                    raise ValueError("El id_administrador asociado a punto_facturacion es None")
            else:
                raise ValueError("El punto de facturación es None")
        except ObjectDoesNotExist:
            raise ValueError("No se encontró ningún registro en Codigosri")       
class Codigoautorizacion(models.Model):
    id_codigosauto = models.AutoField(primary_key=True)
    id_administrador = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='id_administrador', blank=True, null=True)
    codigo_autorizacion = models.CharField(max_length=49, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    fecha_autorizacion = models.DateField(blank=True, null=True)
    ruc = models.CharField(max_length=13, blank=True, null=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'codigoautorizacion'

    @classmethod
    def obtener_codigo_autorizacion_valido(cls):
        try:
            now = timezone.now().date()  # Obtener solo la fecha actual
            codigo_autorizacion = cls.objects.filter(fecha_vencimiento__gte=now).first()
            if codigo_autorizacion:
                if codigo_autorizacion.fecha_vencimiento <= now:
                    # Si la fecha de vencimiento ya pasó, obtener el siguiente código válido
                    codigo_autorizacion = cls.objects.filter(fecha_vencimiento__gt=now).order_by('fecha_vencimiento').first()
                    if codigo_autorizacion:
                        codigo_autorizacion.fecha_autorizacion = now
                        codigo_autorizacion.save()
                        return codigo_autorizacion.codigo_autorizacion
                    else:
                        return None
                else:
                    return codigo_autorizacion.codigo_autorizacion
            else:
                return None
        except ObjectDoesNotExist:
            return None

class Puntofacturacion(models.Model):
    id_puntofacturacion = models.AutoField(primary_key=True)
    nombrepunto = models.CharField(max_length=100)
    id_mesero = models.ForeignKey('Mesero.Meseros', models.DO_NOTHING, db_column='id_mesero', blank=True, null=True)
    id_administrador = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='id_administrador', blank=True, null=True)
    codigo = models.CharField(max_length=3)
    sestado = models.CharField(max_length=1)
    ruc = models.CharField(max_length=13, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'puntofacturacion'
        