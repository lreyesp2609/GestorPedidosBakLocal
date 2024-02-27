from django.db import models
from Administrador.models import Administrador
from Sucursal.models import Sucursales
from Cliente.models import Clientes
from Mesa.models import Mesas
from Producto.models import *
from Combos.models import *
from CodigoFactura.models import *
#from Promociones.models import Promociones
# Create your models here.
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

class Meseros(models.Model):
    id_mesero = models.AutoField(primary_key=True)
    id_sucursal = models.ForeignKey(Sucursales, models.DO_NOTHING, db_column='id_sucursal')
    id_administrador = models.ForeignKey(Administrador, models.DO_NOTHING, db_column='id_administrador')
    telefono = models.CharField(max_length=10)
    apellido = models.CharField(max_length=300)
    nombre = models.CharField(max_length=300)
    fecha_registro = models.DateTimeField()
    id_cuenta = models.ForeignKey(Cuenta, models.DO_NOTHING, db_column='id_cuenta', blank=True, null=True)
    sestado = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'meseros'

class Pedidos(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='id_cliente')
    precio = models.DecimalField(max_digits=9, decimal_places=2)
    tipo_de_pedido = models.CharField(max_length=1)
    metodo_de_pago = models.CharField(max_length=1)
    puntos = models.DecimalField(max_digits=3, decimal_places=0)
    fecha_pedido = models.DateTimeField()
    fecha_entrega = models.DateTimeField(blank=True, null=True)
    estado_del_pedido = models.CharField(max_length=1)
    observacion_del_cliente = models.CharField(max_length=500, blank=True, null=True)
    estado_pago = models.CharField(max_length=100, blank=True, null=True)
    imagen = models.BinaryField(blank=True, null=True)


    class Meta:
        managed = False
        db_table = 'pedidos'


class Pedidosmesa(models.Model):
    id_pmesa = models.AutoField(primary_key=True)
    id_mesero = models.ForeignKey(Meseros, models.DO_NOTHING, db_column='id_mesero')
    id_mesa = models.ForeignKey(Mesas, models.DO_NOTHING, db_column='id_mesa')
    id_pedido = models.ForeignKey(Pedidos, models.DO_NOTHING, db_column='id_pedido')

    class Meta:
        managed = False
        db_table = 'pedidosmesa'


class Detallepedidos(models.Model):
    id_detallepedido = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey(Pedidos, models.DO_NOTHING, db_column='id_pedido')
    id_producto = models.ForeignKey(Producto, models.DO_NOTHING, db_column='id_producto', blank=True, null=True)
    id_combo = models.ForeignKey(Combo, models.DO_NOTHING, db_column='id_combo', blank=True, null=True)
    #id_promocion = models.ForeignKey(Promociones, models.DO_NOTHING, db_column='id_promocion', blank=True, null=True)
    cantidad = models.DecimalField(max_digits=65535, decimal_places=65535)
    precio_unitario = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    impuesto = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    descuento = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'detallepedidos'


class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    id_pedido = models.ForeignKey('Pedidos', models.DO_NOTHING, db_column='id_pedido', blank=True, null=True)
    id_cliente = models.ForeignKey(Clientes, models.DO_NOTHING, db_column='id_cliente', blank=True, null=True)
    id_mesero = models.ForeignKey('Meseros', models.DO_NOTHING, db_column='id_mesero', blank=True, null=True)
    fecha_emision = models.DateTimeField(blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    a_pagar = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    codigo_factura = models.CharField(max_length=15, blank=True, null=True)
    codigo_autorizacion = models.CharField(max_length=49, blank=True, null=True)
    numero_factura_desde = models.CharField(max_length=9)
    numero_factura_hasta = models.CharField(max_length=9)
    estado = models.CharField(max_length=1, choices=[('P', 'P'), ('V', 'V'), ('R', 'R')])
    
    class Meta:
        managed = False
        db_table = 'factura'


class DetalleFactura(models.Model):
    id_detallefactura = models.AutoField(primary_key=True)
    id_factura = models.ForeignKey(Factura, on_delete=models.CASCADE, db_column='id_factura')
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE, db_column='id_producto', blank=True, null=True)
    id_combo = models.ForeignKey(Combo, on_delete=models.CASCADE, db_column='id_combo', blank=True, null=True)
    #id_promocion = models.ForeignKey(Promociones, on_delete=models.CASCADE, db_column='id_promocion', blank=True, null=True)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'detallefactura'

class NotaCredito(models.Model):
    id_notacredito = models.AutoField(primary_key=True)
    id_factura = models.IntegerField()
    id_cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    fechaemision = models.DateTimeField()
    motivo = models.CharField(max_length=500)
    estado = models.CharField(max_length=1, choices=[('A', 'A'), ('C', 'C')])

    class Meta:
        managed = False
        db_table = 'notacredito'