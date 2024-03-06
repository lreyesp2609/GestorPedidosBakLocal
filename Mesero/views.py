import json
import traceback
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.db import transaction
from datetime import datetime
from Mesero.models import *
from decimal import Decimal
from Mesa.models import Mesas
from Inventario.models import *
from .models import Sucursales

@method_decorator(csrf_exempt, name='dispatch')
class ListaPedidos(View):
    def get(self, request, *args, **kwargs):
        try:
            # Obtén la lista de pedidos con información del cliente y detalle del pedido
            pedidos = Pedidos.objects.filter(estado_del_pedido='O')

            # Formatea los datos
            data = []
            for pedido in pedidos:
                detalle_pedido_data = []
                for detalle_pedido in pedido.detallepedidos_set.all():
                    producto_data = {
                        'id_producto': detalle_pedido.id_producto.id_producto,
                        'nombreproducto': detalle_pedido.id_producto.nombreproducto,
                        'cantidad': detalle_pedido.cantidad,
                        'precio_unitario': detalle_pedido.precio_unitario,
                        'impuesto': detalle_pedido.impuesto,
                        'descuento': detalle_pedido.descuento,
                    }
                    detalle_pedido_data.append(producto_data)

                pedido_data = {
                    'id_pedido': pedido.id_pedido,
                    'cliente': {
                        'id_cliente': pedido.id_cliente.id_cliente,
                        'crazon_social': pedido.id_cliente.crazon_social,
                        'ctelefono': pedido.id_cliente.ctelefono,
                        'snombre': pedido.id_cliente.snombre,
                        'capellido': pedido.id_cliente.capellido,
                        'ccorreo_electronico': pedido.id_cliente.ccorreo_electronico,
                    },
                    'precio': pedido.precio,
                    'tipo_de_pedido': pedido.tipo_de_pedido,
                    'metodo_de_pago': pedido.metodo_de_pago,
                    'puntos': pedido.puntos,
                    'fecha_pedido': pedido.fecha_pedido,
                    'fecha_entrega': pedido.fecha_entrega,
                    'estado_del_pedido': pedido.estado_del_pedido,
                    'observacion_del_cliente': pedido.observacion_del_cliente,
                    'detalle_pedido': detalle_pedido_data,
                }

                data.append(pedido_data)

            return JsonResponse({'pedidos': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
@method_decorator(csrf_exempt, name='dispatch')
class ConfirmarPedido(View):
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                id_pedido = request.POST.get('id_pedido')
                pedido = Pedidos.objects.get(id_pedido=id_pedido)
                pedido.estado_del_pedido = 'E'
                pedido.save()

                # Cambiar el estado de los movimientos relacionados con este pedido a 0 si son de tipo 'P'
                movimientos_relacionados = MovimientoInventario.objects.filter(id_pedido=id_pedido, tipomovimiento='P', sestado='1')
                for movimiento_relacionado in movimientos_relacionados:
                    movimiento_relacionado.sestado = '0'
                    movimiento_relacionado.save()

                return JsonResponse({'mensaje': 'Pedido confirmado'})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=400)

        
@method_decorator(csrf_exempt, name='dispatch')
class ListaPedidosMesero(View):
    def get(self, request, *args, **kwargs):
        try:
            pedidos = Pedidos.objects.filter(estado_del_pedido__in=['O', 'P'])

            # Formatea los datos
            data = []
            for pedido in pedidos:
                detalle_pedido_data = []
                for detalle_pedido in pedido.detallepedidos_set.all():
                    producto_data = {
                        'id_producto': detalle_pedido.id_producto.id_producto,
                        'nombreproducto': detalle_pedido.id_producto.nombreproducto,
                        'cantidad': detalle_pedido.cantidad,
                        'precio_unitario': detalle_pedido.precio_unitario,
                        'impuesto': detalle_pedido.impuesto,
                        'descuento': detalle_pedido.descuento,
                    }
                    detalle_pedido_data.append(producto_data)

                # Verifica si el pedido está asociado a una mesa
                mesa_asociada = Pedidosmesa.objects.filter(id_pedido=pedido.id_pedido).first()
                mesa_data = None

                if mesa_asociada:
                    mesa_data = {
                        'id_mesa': mesa_asociada.id_mesa.id_mesa,
                        'observacion': mesa_asociada.id_mesa.observacion,
                        'estado': mesa_asociada.id_mesa.estado,
                        'activa': mesa_asociada.id_mesa.activa,
                        'maxpersonas': mesa_asociada.id_mesa.maxpersonas,
                        'sestado': mesa_asociada.id_mesa.sestado,
                    }

                pedido_data = {
                    'id_pedido': pedido.id_pedido,
                    'cliente': {
                        'id_cliente': pedido.id_cliente.id_cliente,
                        'crazon_social': pedido.id_cliente.crazon_social,
                        'ctelefono': pedido.id_cliente.ctelefono,
                        'snombre': pedido.id_cliente.snombre,
                        'capellido': pedido.id_cliente.capellido,
                        'ccorreo_electronico': pedido.id_cliente.ccorreo_electronico,
                    },
                    'precio': pedido.precio,
                    'tipo_de_pedido': pedido.tipo_de_pedido,
                    'metodo_de_pago': pedido.metodo_de_pago,
                    'puntos': pedido.puntos,
                    'fecha_pedido': pedido.fecha_pedido,
                    'fecha_entrega': pedido.fecha_entrega,
                    'estado_del_pedido': pedido.estado_del_pedido,
                    'observacion_del_cliente': pedido.observacion_del_cliente,
                    'detalle_pedido': detalle_pedido_data,
                    'mesa_asociada': mesa_data,
                }

                data.append(pedido_data)

            return JsonResponse({'pedidos': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
@method_decorator(csrf_exempt, name='dispatch')
class TodosLosPedidos(View):
    def get(self, request, *args, **kwargs):
        try:
            pedidos = Pedidos.objects.all().values()
            pedidos_list = list(pedidos)
            return JsonResponse({'todos_los_pedidos': pedidos_list})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
from decimal import Decimal

@method_decorator(csrf_exempt, name='dispatch')
class TomarPedido(View):
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                id_usuario = kwargs.get('id_cuenta')
                mesero = Meseros.objects.get(id_cuenta=id_usuario)
                id_mesero = mesero.id_mesero
                id_sucursal = mesero.id_sucursal_id  # Obtener el id_sucursal del mesero

                id_mesa = request.POST.get('id_mesa')
                id_cliente_id = request.POST.get('id_cliente')
                fecha_pedido = datetime.now()
                tipo_de_pedido = request.POST.get('tipo_de_pedido')
                metodo_de_pago = request.POST.get('metodo_de_pago')
                puntos = request.POST.get('puntos')
                fecha_entrega = request.POST.get('fecha_entrega', None)
                estado_del_pedido = request.POST.get('estado_del_pedido')
                observacion_del_cliente = request.POST.get('observacion_del_cliente')

                cliente_instance = get_object_or_404(Clientes, id_cliente=id_cliente_id)

                estado_pago = "En Revisión"
                mesero_instance = get_object_or_404(Meseros, id_mesero=id_mesero)
                nuevo_pedido = Pedidos.objects.create(
                    id_cliente=cliente_instance,
                    precio=0,
                    tipo_de_pedido=tipo_de_pedido,
                    metodo_de_pago=metodo_de_pago,
                    puntos=puntos,
                    fecha_pedido=fecha_pedido,
                    fecha_entrega=fecha_entrega,
                    estado_del_pedido=estado_del_pedido,
                    estado_pago=estado_pago,
                    observacion_del_cliente=observacion_del_cliente,
                )

                
                mesa_instance = get_object_or_404(Mesas, id_mesa=id_mesa)
                Pedidosmesa.objects.create(
                    id_mesero=mesero_instance,
                    id_mesa=mesa_instance,
                    id_pedido=nuevo_pedido,
                )

                detalles_pedido_raw = request.POST.get('detalles_pedido', '{}')
                detalles_pedido = json.loads(detalles_pedido_raw)

                total_precio_pedido = Decimal(0)
                total_descuento = Decimal(0)

                # Crear los detalles de detalle de pedido
                for detalle_pedido_data in detalles_pedido['detalles_pedido']:
                    id_producto_id = detalle_pedido_data.get('id_producto')
                    id_combo_id = detalle_pedido_data.get('id_combo')
                    precio_unitario = detalle_pedido_data['precio_unitario']
                    # Convertir el precio_unitario_raw a un número decimal
                    # Impuesto establecido en 0 para evitar que se calcule
                    impuesto = Decimal(0)
                    cantidad = Decimal(detalle_pedido_data['cantidad'])
                    descuento = Decimal(detalle_pedido_data.get('descuento', 0))

                    precio_total_detalle = (precio_unitario + impuesto) * cantidad - descuento
                    total_precio_pedido += precio_total_detalle
                    total_descuento += descuento

                    if id_producto_id and not id_combo_id:  # Es un producto individual
                        producto_instance = get_object_or_404(Producto, id_producto=id_producto_id)
                        Detallepedidos.objects.create(
                            id_pedido=nuevo_pedido,
                            id_producto=producto_instance,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            impuesto=impuesto,
                            descuento=descuento,
                        )
                    elif id_combo_id and not id_producto_id:  # Es un combo
                        combo_instance = get_object_or_404(Combo, id_combo=id_combo_id)
                        Detallepedidos.objects.create(
                            id_pedido=nuevo_pedido,
                            id_combo=combo_instance,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            impuesto=impuesto,
                            descuento=descuento,
                        )

                # Calcular el subtotal y el total del pedido
                subtotal = total_precio_pedido - total_descuento  # Subtotal = Total - Descuento

                # El impuesto en la factura se calcula correctamente
                iva_factura = subtotal * Decimal('0.12')
                a_pagar = subtotal + iva_factura  # A pagar = Subtotal + 12% IVA

                # Guardar el monto a pagar en lugar del total
                nuevo_pedido.precio = a_pagar
                nuevo_pedido.save()

                nueva_factura = Factura.objects.create(
                    id_pedido=nuevo_pedido,
                    id_cliente=cliente_instance,
                    id_mesero=mesero_instance,
                    total=total_precio_pedido,
                    iva=iva_factura,
                    descuento=total_descuento,
                    subtotal=subtotal,
                    a_pagar=a_pagar,
                    codigo_autorizacion=Codigoautorizacion.obtener_codigo_autorizacion_valido(),
                    fecha_emision=datetime.now(),
                    estado='P'
                )
                # Crear los detalles de la factura
                for detalle_pedido_data in detalles_pedido['detalles_pedido']:
                    id_producto_id = detalle_pedido_data.get('id_producto')
                    id_combo_id = detalle_pedido_data.get('id_combo')
                    cantidad = Decimal(detalle_pedido_data['cantidad'])
                    precio_unitario = detalle_pedido_data['precio_unitario']
                    descuento = Decimal(detalle_pedido_data.get('descuento', 0))
                    valor = (precio_unitario * cantidad) - descuento

                    if id_producto_id and not id_combo_id:  # Es un producto individual
                        id_producto_instance = get_object_or_404(Producto, id_producto=id_producto_id)
                        DetalleFactura.objects.create(
                            id_factura=nueva_factura,
                            id_producto=id_producto_instance,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            descuento=descuento,
                            valor=valor,
                        )
                    elif id_combo_id and not id_producto_id:  # Es un combo
                        id_combo_instance = get_object_or_404(Combo, id_combo=id_combo_id)
                        DetalleFactura.objects.create(
                            id_factura=nueva_factura,
                            id_combo=id_combo_instance,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            descuento=descuento,
                            valor=valor,
                        )

                return JsonResponse({'mensaje': 'Pedido y factura creados con éxito'})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'No se encontró ningún registro en Codigosri'}, status=400)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class TomarPedidoSinMesa(View):
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                id_usuario = kwargs.get('id_cuenta')
                mesero = Meseros.objects.get(id_cuenta=id_usuario)
                id_mesero = mesero.id_mesero
                id_sucursal = mesero.id_sucursal_id  # Obtener el id_sucursal del mesero
                id_cliente_id = request.POST.get('id_cliente')
                fecha_pedido = datetime.now()
                tipo_de_pedido = request.POST.get('tipo_de_pedido')
                metodo_de_pago = request.POST.get('metodo_de_pago')
                puntos = request.POST.get('puntos')
                fecha_entrega = request.POST.get('fecha_entrega', None)
                estado_del_pedido = request.POST.get('estado_del_pedido')
                observacion_del_cliente = request.POST.get('observacion_del_cliente')
                
                cliente_instance = get_object_or_404(Clientes, id_cliente=id_cliente_id)

                nuevo_pedido = Pedidos.objects.create(
                    id_cliente=cliente_instance,
                    precio=0,
                    tipo_de_pedido=tipo_de_pedido,
                    metodo_de_pago=metodo_de_pago,
                    puntos=puntos,
                    fecha_pedido=fecha_pedido,
                    fecha_entrega=fecha_entrega,
                    estado_del_pedido=estado_del_pedido,
                    observacion_del_cliente=observacion_del_cliente,
                )
                mesero_instance = get_object_or_404(Meseros, id_mesero=id_mesero)
                detalles_pedido_raw = request.POST.get('detalles_pedido', '{}')
                detalles_pedido = json.loads(detalles_pedido_raw)
                total_precio_pedido = Decimal(0)
                total_descuento = Decimal(0)
                # Crear los detalles de detalle de pedido
                for detalle_pedido_data in detalles_pedido['detalles_pedido']:
                    id_producto_id = detalle_pedido_data.get('id_producto')
                    id_combo_id = detalle_pedido_data.get('id_combo')
                    precio_unitario = Decimal(detalle_pedido_data['precio_unitario'])
                    # Impuesto establecido en 0 para evitar que se calcule
                    impuesto = Decimal(0)
                    cantidad = Decimal(detalle_pedido_data['cantidad'])
                    descuento = Decimal(detalle_pedido_data.get('descuento', 0))

                    precio_total_detalle = (precio_unitario + impuesto) * cantidad - descuento
                    total_precio_pedido += precio_total_detalle
                    total_descuento += descuento

                    if id_producto_id and not id_combo_id:  # Es un producto individual
                        producto_instance = get_object_or_404(Producto, id_producto=id_producto_id)
                        Detallepedidos.objects.create(
                            id_pedido=nuevo_pedido,
                            id_producto=producto_instance,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            impuesto=impuesto,
                            descuento=descuento,
                        )
                    elif id_combo_id and not id_producto_id:  # Es un combo
                        combo_instance = get_object_or_404(Combo, id_combo=id_combo_id)
                        Detallepedidos.objects.create(
                            id_pedido=nuevo_pedido,
                            id_combo=combo_instance,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            impuesto=impuesto,
                            descuento=descuento,
                        )

                # Calcular el subtotal y el total del pedido
                subtotal = total_precio_pedido - total_descuento  # Subtotal = Total - Descuento
                iva_factura = subtotal * Decimal('0.12')
                a_pagar = subtotal + iva_factura  # A pagar = Subtotal + 12% IVA
                nuevo_pedido.precio = a_pagar
                nuevo_pedido.save()

                # Crear la factura asociada al pedido
                numero_factura, numero_factura_desde, numero_factura_hasta = Codigosri.obtener_proximo_numero_factura(id_mesero, id_sucursal)
                nueva_factura = Factura.objects.create(
                    id_pedido=nuevo_pedido,
                    id_cliente=cliente_instance,
                    id_mesero=mesero_instance,
                    total=total_precio_pedido,
                    iva=iva_factura,
                    descuento=total_descuento,
                    subtotal=subtotal,
                    a_pagar=a_pagar,
                    codigo_factura=numero_factura,
                    codigo_autorizacion=Codigoautorizacion.obtener_codigo_autorizacion_valido(),
                    fecha_emision=datetime.now(),
                    numero_factura_desde=numero_factura_desde,  # Asigna el valor devuelto por el método
                    numero_factura_hasta=numero_factura_hasta,  # Asigna el valor devuelto por el método
                )



                # Crear los detalles de la factura
                for detalle_pedido_data in detalles_pedido['detalles_pedido']:
                    id_producto_id = detalle_pedido_data.get('id_producto')
                    id_combo_id = detalle_pedido_data.get('id_combo')
                    cantidad = Decimal(detalle_pedido_data['cantidad'])
                    precio_unitario = Decimal(detalle_pedido_data['precio_unitario'])
                    descuento = Decimal(detalle_pedido_data.get('descuento', 0))
                    valor = (precio_unitario * cantidad) - descuento

                    if id_producto_id and not id_combo_id:  # Es un producto individual
                        id_producto_instance = get_object_or_404(Producto, id_producto=id_producto_id)
                        DetalleFactura.objects.create(
                            id_factura=nueva_factura,
                            id_producto=id_producto_instance,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            descuento=descuento,
                            valor=valor,
                        )
                    elif id_combo_id and not id_producto_id:  # Es un combo
                        id_combo_instance = get_object_or_404(Combo, id_combo=id_combo_id)
                        DetalleFactura.objects.create(
                            id_factura=nueva_factura,
                            id_combo=id_combo_instance,
                            cantidad=cantidad,
                            precio_unitario=precio_unitario,
                            descuento=descuento,
                            valor=valor,
                        )

                return JsonResponse({'mensaje': 'Pedido y factura creados con éxito'})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=400)
def ver_factura(request, id_pedido):
    print("ID de pedido recibido:", id_pedido)
    try:
        print('aver')
        factura = Factura.objects.get(id_pedido_id=id_pedido)
        detalles_factura = DetalleFactura.objects.filter(id_factura_id=factura.id_factura).values()

        detalles_factura_list = list(detalles_factura)
        id_cliente = factura.id_cliente_id
        print('aver')
        # Obtener información del pedido
        pedido = Pedidos.objects.get(pk=id_pedido)
        print('averx')
        tipo_de_pedido = pedido.tipo_de_pedido
        print('averx1')
        metodo_de_pago = pedido.metodo_de_pago
        print('aver2')
        # Obtener la información de la factura
        codigo_autorizacion_sri = factura.codigo_autorizacion
        print('averx3')
        codigo_autorizacion_obj = Codigoautorizacion.objects.get(codigo_autorizacion=codigo_autorizacion_sri)
        print('averx4')
        fecha_autorizacion = codigo_autorizacion_obj.fecha_autorizacion
        print('averx5')
        fecha_vencimiento = codigo_autorizacion_obj.fecha_vencimiento
        print('aver3')
        # Obtener la numeración desde el modelo Codigosri
        numeracion = f"{factura.numero_factura_desde}-{factura.numero_factura_hasta}"
        print('aver4')
        factura_data = {
            'id_factura': factura.id_factura,
            'id_cliente': id_cliente,
            'codigo_factura': factura.codigo_factura,
            'codigo_autorizacion_sri': codigo_autorizacion_sri,
            'autorizacion': fecha_autorizacion,
            'vencimiento': fecha_vencimiento,
            'numeracion': numeracion,
            'fecha_emision': factura.fecha_emision,
            'a_pagar': factura.a_pagar,
            'iva': factura.iva,
            'total': factura.total,
            'descuento': factura.descuento,
            'subtotal': factura.subtotal,
            'tipo_de_pedido': tipo_de_pedido,
            'metodo_de_pago': metodo_de_pago,  
            'detalles_factura': detalles_factura_list,
        }
        print('aver5')
        return JsonResponse(factura_data)
    except Factura.DoesNotExist:
        return JsonResponse({'error': 'La factura no existe'}, status=404)


def pedidos_del_mesero(request, id_mesa, **kwargs):
    try:
        id_usuario = kwargs.get('id_cuenta')
        id_mesero = Meseros.objects.get(id_cuenta=id_usuario)
        
        # Obtener todos los pedidos asociados al mesero y a la mesa
        pedidos_del_mesero = Pedidosmesa.objects.filter(id_mesero=id_mesero, id_mesa=id_mesa)

        # Inicializar una lista para almacenar la información de los pedidos
        pedidos_info = []

        # Iterar sobre cada pedido asociado al mesero y a la mesa
        for pedido_mesa in pedidos_del_mesero:
            # Obtener la información del pedido
            pedido_info = {
                'id_pedido': pedido_mesa.id_pedido.id_pedido,
                'id_mesa': pedido_mesa.id_mesa.id_mesa,
                'fecha_pedido': pedido_mesa.id_pedido.fecha_pedido,
                # Otros campos del pedido que quieras mostrar
            }
            pedidos_info.append(pedido_info)

        return JsonResponse({'pedidos_del_mesero': pedidos_info})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
    
class ObtenerMeseroView(View):
    def get(self, request, *args, **kwargs):
        try:
            id_usuario = kwargs.get('id_usuario')
            
            if id_usuario:
                mesero = get_object_or_404(Meseros, id_cuenta=id_usuario)

                mesero_data = {
                    'id_mesero': mesero.id_mesero,
                    'id_sucursal': mesero.id_sucursal.id_sucursal,
                    'id_administrador': mesero.id_administrador.id_administrador,
                    'telefono': mesero.telefono,
                    'apellido': mesero.apellido,
                    'nombre': mesero.nombre,
                    'fecha_registro': mesero.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
                    'id_cuenta': mesero.id_cuenta.id_cuenta if mesero.id_cuenta else None,
                    'sestado': mesero.sestado,
                }

                return JsonResponse({'mesero': mesero_data})
            else:
                # Si no se proporciona un ID de usuario, retorna un error
                return JsonResponse({'error': 'ID de usuario no proporcionado'}, status=400)

        except Cuenta.DoesNotExist:
            return JsonResponse({'error': 'Cuenta no encontrada'}, status=404)

        except Meseros.DoesNotExist:
            return JsonResponse({'error': 'Mesero no encontrado'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
@method_decorator(csrf_exempt, name='dispatch')
class ListaMeseros(View):
    def get(self, request, *args, **kwargs):
        try:
            # Obtén la lista de meseros
            meseros = Meseros.objects.all()

            # Formatea los datos
            data = []
            for mesero in meseros:
                mesero_data = {
                    'id_mesero': mesero.id_mesero,
                    'id_sucursal': mesero.id_sucursal.id_sucursal,
                    'id_administrador': mesero.id_administrador.id_administrador,
                    'nombre': mesero.nombre,
                    'apellido': mesero.apellido,
                    'telefono': mesero.telefono,
                    'fecha_registro': mesero.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
                    'sestado': mesero.sestado,
                }
                data.append(mesero_data)

            return JsonResponse({'meseros': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
        

@method_decorator(csrf_exempt, name='dispatch')
class ListaFacturas(View):
    def get(self, request, *args, **kwargs):
        try:
            # Obtén la lista de facturas
            facturas = Factura.objects.all()

            # Formatea los datos
            data = []
            for factura in facturas:
                pedido = factura.id_pedido
                estado_pago = pedido.estado_pago if pedido else None
                tipo_de_pedido = pedido.tipo_de_pedido if pedido else None

                factura_data = {
                    'id_factura': factura.id_factura,
                    'id_pedido': factura.id_pedido.id_pedido if factura.id_pedido else None,
                    'id_cliente': factura.id_cliente.id_cliente if factura.id_cliente else None,
                    'id_mesero': factura.id_mesero.id_mesero if factura.id_mesero else None,
                    'fecha_emision': factura.fecha_emision.strftime('%Y-%m-%d %H:%M:%S') if factura.fecha_emision else None,
                    'total': str(factura.total),
                    'iva': str(factura.iva) if factura.iva else None,
                    'descuento': str(factura.descuento) if factura.descuento else None,
                    'subtotal': str(factura.subtotal) if factura.subtotal else None,
                    'a_pagar': str(factura.a_pagar) if factura.a_pagar else None,
                    'codigo_factura': factura.codigo_factura,
                    'codigo_autorizacion': factura.codigo_autorizacion,
                    'numero_factura_desde': factura.numero_factura_desde,
                    'numero_factura_hasta': factura.numero_factura_hasta,
                    'estado_pago': estado_pago,
                    'tipo_de_pedido': tipo_de_pedido,
                    'estado': factura.estado
                }
                data.append(factura_data)

            return JsonResponse({'facturas': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

@method_decorator(csrf_exempt, name='dispatch')
class DetalleFacturaView(View):
    def get(self, request, id_factura, *args, **kwargs):
        try:
            # Obtén el detalle de la factura
            detalle_factura = DetalleFactura.objects.filter(id_factura=id_factura)

            # Formatea los datos
            data = []
            for detalle in detalle_factura:
                detalle_data = {
                    'id_detallefactura': detalle.id_detallefactura,
                    'id_factura': detalle.id_factura.id_factura if detalle.id_factura else None,
                    'id_producto': detalle.id_producto.id_producto if detalle.id_producto else None,
                    'id_combo': detalle.id_combo.id_combo if detalle.id_combo else None,
                    'cantidad': str(detalle.cantidad),
                    'precio_unitario': str(detalle.precio_unitario),
                    'descuento': str(detalle.descuento),
                    'valor': str(detalle.valor)
                }
                data.append(detalle_data)

            return JsonResponse({'detalle_factura': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ListaFacturasConDetalles(View):
    def get(self, request, *args, **kwargs):
        try:
            # Obtén la lista de facturas
            facturas = Factura.objects.all()

            # Formatea los datos de las facturas y sus detalles
            data = []
            for factura in facturas:
                pedido = factura.id_pedido
                estado_pago = pedido.estado_pago if pedido else None
                tipo_de_pedido = pedido.tipo_de_pedido if pedido else None

                factura_data = {
                    'id_factura': factura.id_factura,
                    'id_pedido': factura.id_pedido.id_pedido if factura.id_pedido else None,
                    'id_cliente': factura.id_cliente.id_cliente if factura.id_cliente else None,
                    'id_mesero': factura.id_mesero.id_mesero if factura.id_mesero else None,
                    'fecha_emision': factura.fecha_emision.strftime('%Y-%m-%d %H:%M:%S') if factura.fecha_emision else None,
                    'total': str(factura.total),
                    'iva': str(factura.iva) if factura.iva else None,
                    'descuento': str(factura.descuento) if factura.descuento else None,
                    'subtotal': str(factura.subtotal) if factura.subtotal else None,
                    'a_pagar': str(factura.a_pagar) if factura.a_pagar else None,
                    'codigo_factura': factura.codigo_factura,
                    'codigo_autorizacion': factura.codigo_autorizacion,
                    'numero_factura_desde': factura.numero_factura_desde,
                    'numero_factura_hasta': factura.numero_factura_hasta,
                    'estado_pago': estado_pago,
                    'tipo_de_pedido': tipo_de_pedido,
                    'estado': factura.estado
                }

                # Obtén los detalles de la factura
                detalles_factura = DetalleFactura.objects.filter(id_factura=factura.id_factura)
                detalles_data = []
                for detalle in detalles_factura:
                    # Obtén el nombre del producto
                    if detalle.id_producto:
                        producto = Producto.objects.get(id_producto=detalle.id_producto.id_producto)
                        nombre_producto = producto.nombreproducto
                    else:
                        nombre_producto = None

                    detalle_data = {
                        'id_detallefactura': detalle.id_detallefactura,
                        'id_producto': detalle.id_producto.id_producto if detalle.id_producto else None,
                        'id_combo': detalle.id_combo.id_combo if detalle.id_combo else None,
                        'cantidad': str(detalle.cantidad),
                        'precio_unitario': str(detalle.precio_unitario),
                        'descuento': str(detalle.descuento),
                        'valor': str(detalle.valor),
                        'nombre_producto': nombre_producto  # Agregar el nombre del producto
                    }
                    detalles_data.append(detalle_data)

                factura_data['detalles_factura'] = detalles_data
                data.append(factura_data)

            return JsonResponse({'facturas_con_detalles': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class ListaNotasCredito(View):
    def get(self, request, id_notacredito, *args, **kwargs):
        try:
            # Obtén la nota de crédito específica
            nota_credito = NotaCredito.objects.get(id_notacredito=id_notacredito)

            # Formatea los datos
            nota_credito_data = {
                'id_notacredito': nota_credito.id_notacredito,
                'id_factura': nota_credito.id_factura,
                'fecha_emision': nota_credito.fechaemision.strftime('%Y-%m-%d %H:%M:%S') if nota_credito.fechaemision else None,
                'motivo': nota_credito.motivo,
                'estado': nota_credito.estado
            }

            return JsonResponse({'nota_credito': nota_credito_data})
        except NotaCredito.DoesNotExist:
            return JsonResponse({'error': 'La nota de crédito especificada no existe'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

@method_decorator(csrf_exempt, name='dispatch')
class FacturaDetallesNotaCredito(View):
    def get(self, request, id_factura, *args, **kwargs):
        try:
            # Obtén los detalles de la factura
            factura = Factura.objects.get(id_factura=id_factura)
            pedido = factura.id_pedido
            estado_pago = pedido.estado_pago if pedido else None
            tipo_de_pedido = pedido.tipo_de_pedido if pedido else None

            factura_data = {
                'id_factura': factura.id_factura,
                'id_pedido': factura.id_pedido.id_pedido if factura.id_pedido else None,
                'id_cliente': factura.id_cliente.id_cliente if factura.id_cliente else None,
                'id_mesero': factura.id_mesero.id_mesero if factura.id_mesero else None,
                'fecha_emision': factura.fecha_emision.strftime('%Y-%m-%d %H:%M:%S') if factura.fecha_emision else None,
                'total': str(factura.total),
                'iva': str(factura.iva) if factura.iva else None,
                'descuento': str(factura.descuento) if factura.descuento else None,
                'subtotal': str(factura.subtotal) if factura.subtotal else None,
                'a_pagar': str(factura.a_pagar) if factura.a_pagar else None,
                'codigo_factura': factura.codigo_factura,
                'codigo_autorizacion': factura.codigo_autorizacion,
                'numero_factura_desde': factura.numero_factura_desde,
                'numero_factura_hasta': factura.numero_factura_hasta,
                'estado_pago': estado_pago,
                'tipo_de_pedido': tipo_de_pedido,
                'estado': factura.estado
            }

            # Obtén los detalles de la factura
            detalles_factura = DetalleFactura.objects.filter(id_factura=factura.id_factura)
            detalles_data = []
            for detalle in detalles_factura:
                    # Obtén el nombre del producto
                    if detalle.id_producto:
                        producto = Producto.objects.get(id_producto=detalle.id_producto.id_producto)
                        nombre_producto = producto.nombreproducto
                    else:
                        nombre_producto = None

                    detalle_data = {
                        'id_detallefactura': detalle.id_detallefactura,
                        'id_producto': detalle.id_producto.id_producto if detalle.id_producto else None,
                        'id_combo': detalle.id_combo.id_combo if detalle.id_combo else None,
                        'cantidad': str(detalle.cantidad),
                        'precio_unitario': str(detalle.precio_unitario),
                        'descuento': str(detalle.descuento),
                        'valor': str(detalle.valor),
                        'nombre_producto': nombre_producto  # Agregar el nombre del producto
                    }
                    detalles_data.append(detalle_data)
                    factura_data['detalles_factura'] = detalles_data

            # Obtén los detalles de la nota de crédito asociada (si existe)
            nota_credito = NotaCredito.objects.filter(id_factura=id_factura).first()
            if nota_credito:
                nota_credito_data = {
                    'id_notacredito': nota_credito.id_notacredito,
                    'id_factura': nota_credito.id_factura,
                    'fecha_emision': nota_credito.fechaemision.strftime('%Y-%m-%d %H:%M:%S') if nota_credito.fechaemision else None,
                    'motivo': nota_credito.motivo,
                    'estado': nota_credito.estado
                }
            else:
                nota_credito_data = None

            return JsonResponse({'factura': factura_data, 'nota_credito': nota_credito_data})
        except Factura.DoesNotExist:
            return JsonResponse({'error': 'La factura especificada no existe'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        
@method_decorator(csrf_exempt, name='dispatch')
class CrearReversoFactura(View):
    def post(self, request, id_factura):
        try:
            with transaction.atomic():
                # Obtener la factura original
                factura_original = get_object_or_404(Factura, id_factura=id_factura)
                
                # Obtener el motivo del reverso desde el cuerpo de la solicitud JSON
                body_unicode = request.body.decode('utf-8')
                body_data = json.loads(body_unicode)
                motivo_reverso = body_data.get('motivo_reverso')
                if not motivo_reverso:
                    return JsonResponse({'error': 'El motivo del reverso es obligatorio'}, status=400)

                # Crear el reverso de la factura
                reverso = NotaCredito.objects.create(
                    id_factura=factura_original.id_factura,
                    fechaemision=datetime.now(),
                    motivo=motivo_reverso,
                    estado='A'
                )

                # Cambiar el estado de la factura original a 'R' (Reversada)
                factura_original.estado = 'R'
                factura_original.save()
                
                # Obtener el pedido asociado con la factura
                pedido = factura_original.id_pedido
                
                # Obtener los movimientos de inventario asociados con el pedido
                movimientos_origen = MovimientoInventario.objects.filter(id_pedido=pedido)
                
                # Cambiar el estado del pedido a 'R' (Reversado)
                pedido.estado_del_pedido = 'R'
                pedido.estado_pago = 'Denegado'  # Actualizar el estado_pago a 'denegado'
                pedido.save()
                
                # Iterar sobre los movimientos de inventario asociados con el pedido
                for movimiento_origen in movimientos_origen:
                    # Crear el movimiento de reversion
                    nuevo_movimiento_reversion = MovimientoInventario.objects.create(
                        id_cuenta=movimiento_origen.id_cuenta,
                        id_pedido=movimiento_origen.id_pedido,
                        id_bodega=movimiento_origen.id_bodega,
                        tipomovimiento='R',
                        sestado='1',  # Establecer el sestado como '1'
                        observacion=f'Pedido reversado: {factura_original.codigo_factura}'
                    )
                    
                    # Modificar el sestado del movimiento original a '0'
                    movimiento_origen.sestado = '0'
                    movimiento_origen.save()
                    
                    # Copiar los detalles del movimiento original al nuevo movimiento
                    detalles_origen = DetalleMovimientoInventario.objects.filter(id_movimientoinventario=movimiento_origen)
                    for detalle_origen in detalles_origen:
                        DetalleMovimientoInventario.objects.create(
                            id_movimientoinventario=nuevo_movimiento_reversion,
                            id_articulo=detalle_origen.id_articulo,
                            id_producto=detalle_origen.id_producto,
                            cantidad=detalle_origen.cantidad,
                            tipo=detalle_origen.tipo
                        )
                        
                        # Actualizar el inventario
                        producto_instance = detalle_origen.id_producto
                        componente_instance = detalle_origen.id_articulo

                        inventario, created = Inventario.objects.get_or_create(
                            id_bodega=movimiento_origen.id_bodega,
                            id_producto=producto_instance,
                            id_componente=componente_instance,
                            defaults={'cantidad_disponible': detalle_origen.cantidad, 'costo_unitario': None}
                        )

                        if not created:
                            inventario.cantidad_disponible += detalle_origen.cantidad
                            inventario.save()

                return JsonResponse({'mensaje': 'Reverso de factura creado con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class FacturasValidadasReportes(View):
    def get(self, request, *args, **kwargs):
        try:
            # Obtén la lista de facturas validadas
            facturas_validadas = Factura.objects.filter(
                codigo_factura__isnull=False,
                numero_factura_desde__isnull=False,
                numero_factura_hasta__isnull=False
            )

            # Formatea los datos
            data = []
            for factura in facturas_validadas:
                factura_data = {
                    'codigo_factura': str(factura.codigo_factura) if factura.codigo_factura else None,
                    'cliente_completo': f"{factura.id_cliente.snombre} {factura.id_cliente.capellido}" if factura.id_cliente else None,
                    'fecha_emision': factura.fecha_emision.strftime('%Y-%m-%d %H:%M:%S') if factura.fecha_emision else None,
                    'mesero_completo': f"{factura.id_mesero.nombre} {factura.id_mesero.apellido}" if factura.id_cliente else None,
                    'total': str(factura.total),
                    'iva': str(factura.iva) if factura.iva else None,
                    'descuento': str(factura.descuento) if factura.descuento else None,
                    'subtotal': str(factura.subtotal) if factura.subtotal else None,
                    'a_pagar': str(factura.a_pagar) if factura.a_pagar else None,
                }
                data.append(factura_data)
            return JsonResponse({'facturas_validadas': data})
        except Exception as e:return JsonResponse({'error': str(e)}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class ListaPedidosReportes(View):
    def get(self, request, id_mesero, *args, **kwargs):
        try:
            # Filtrar los pedidos por el mesero proporcionado en la URL
            pedidos = Pedidos.objects.filter(estado_pago='Pagado', factura__id_mesero=id_mesero)

            # Formatear los datos de los pedidos y sus detalles
            data = []
            for pedido in pedidos:
                detalle_pedido_data = []
                for detalle_pedido in pedido.detallepedidos_set.all():
                    producto_data = {
                        'id_producto': detalle_pedido.id_producto.id_producto,
                        'nombreproducto': detalle_pedido.id_producto.nombreproducto,
                        'cantidad': detalle_pedido.cantidad,
                        'precio_unitario': detalle_pedido.precio_unitario,
                        'impuesto': detalle_pedido.impuesto,
                        'descuento': detalle_pedido.descuento,
                    }
                    detalle_pedido_data.append(producto_data)

                pedido_data = {
                    'id_pedido': pedido.id_pedido,
                    'cliente': {
                        'id_cliente': pedido.id_cliente.id_cliente,
                        'crazon_social': pedido.id_cliente.crazon_social,
                        'ctelefono': pedido.id_cliente.ctelefono,
                        'snombre': pedido.id_cliente.snombre,
                        'capellido': pedido.id_cliente.capellido,
                        'ccorreo_electronico': pedido.id_cliente.ccorreo_electronico,
                    },
                    'id_mesero': id_mesero,
                    'nombre_mesero': pedido.factura_set.first().id_mesero.nombre + ' ' + pedido.factura_set.first().id_mesero.apellido,
                    'precio': pedido.precio,
                    'tipo_de_pedido': pedido.tipo_de_pedido,
                    'metodo_de_pago': pedido.metodo_de_pago,
                    'puntos': pedido.puntos,
                    'fecha_pedido': pedido.fecha_pedido,
                    'fecha_entrega': pedido.fecha_entrega,
                    'estado_del_pedido': pedido.estado_del_pedido,
                    'observacion_del_cliente': pedido.observacion_del_cliente,
                    'detalle_pedido': detalle_pedido_data,
                }

                data.append(pedido_data)

            return JsonResponse({'pedidos': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class ListaTodosPedidosReportes(View):
    def get(self, request, *args, **kwargs):
        try:
            # Obtén la lista de pedidos con información del cliente, detalle del pedido y mesero
            pedidos = Pedidos.objects.filter(estado_pago='Pagado').exclude(factura__id_mesero=None)

            # Formatea los datos
            data = []
            for pedido in pedidos:
                detalle_pedido_data = []
                for detalle_pedido in pedido.detallepedidos_set.all():
                    producto_data = {
                        'id_producto': detalle_pedido.id_producto.id_producto,
                        'nombreproducto': detalle_pedido.id_producto.nombreproducto,
                        'cantidad': detalle_pedido.cantidad,
                        'precio_unitario': detalle_pedido.precio_unitario,
                        'impuesto': detalle_pedido.impuesto,
                        'descuento': detalle_pedido.descuento,
                    }
                    detalle_pedido_data.append(producto_data)

                # Obtén el ID del mesero asociado al pedido
                id_mesero = pedido.factura_set.first().id_mesero.id_mesero

                pedido_data = {
                    'id_pedido': pedido.id_pedido,
                    'cliente': {
                        'id_cliente': pedido.id_cliente.id_cliente,
                        'crazon_social': pedido.id_cliente.crazon_social,
                        'ctelefono': pedido.id_cliente.ctelefono,
                        'snombre': pedido.id_cliente.snombre,
                        'capellido': pedido.id_cliente.capellido,
                        'ccorreo_electronico': pedido.id_cliente.ccorreo_electronico,
                    },
                    'id_mesero': id_mesero,  
                    'nombre_mesero': pedido.factura_set.first().id_mesero.nombre + ' ' + pedido.factura_set.first().id_mesero.apellido,
                    'precio': pedido.precio,
                    'tipo_de_pedido': pedido.tipo_de_pedido,
                    'metodo_de_pago': pedido.metodo_de_pago,
                    'puntos': pedido.puntos,
                    'fecha_pedido': pedido.fecha_pedido,
                    'fecha_entrega': pedido.fecha_entrega,
                    'estado_del_pedido': pedido.estado_del_pedido,
                    'observacion_del_cliente': pedido.observacion_del_cliente,
                    'detalle_pedido': detalle_pedido_data,
                }

                data.append(pedido_data)

            return JsonResponse({'pedidos': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
class ListaPedidosSucursalReportes(View):
    def get(self, request, *args, **kwargs):
        try:
            # Obtén la lista de pedidos con información del cliente, detalle del pedido y mesero
            pedidos = Pedidos.objects.filter(estado_pago='Pagado')

            # Obtén la lista de meseros
            meseros = Meseros.objects.all()
            meseros_dict = {mesero.id_mesero: mesero for mesero in meseros}

            # Obtén la lista de sucursales
            sucursales = Sucursales.objects.all()
            sucursales_dict = {sucursal.id_sucursal: sucursal for sucursal in sucursales}

            # Formatea los datos
            data = []
            for pedido in pedidos:
                detalle_pedido_data = []
                for detalle_pedido in pedido.detallepedidos_set.all():
                    producto_data = {
                        'id_producto': detalle_pedido.id_producto.id_producto,
                        'nombreproducto': detalle_pedido.id_producto.nombreproducto,
                        'cantidad': detalle_pedido.cantidad,
                        'precio_unitario': detalle_pedido.precio_unitario,
                        'impuesto': detalle_pedido.impuesto,
                        'descuento': detalle_pedido.descuento,
                    }
                    detalle_pedido_data.append(producto_data)

                # Obtén el ID del mesero asociado al pedido (si existe)
                factura = pedido.factura_set.first()
                id_mesero = factura.id_mesero.id_mesero if factura and factura.id_mesero else None
                mesero_info = None
                if id_mesero:
                    mesero = meseros_dict[id_mesero]
                    mesero_info = {
                        'id_mesero': mesero.id_mesero,
                        'nombre': mesero.nombre,
                        'apellido': mesero.apellido,
                        'telefono': mesero.telefono,
                        'fecha_registro': mesero.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
                        'sestado': mesero.sestado,
                        'id_sucursal': mesero.id_sucursal.id_sucursal,  # Agregar el ID de la sucursal al mesero
                        'nombre_sucursal': mesero.id_sucursal.snombre,  # Agregar el nombre de la sucursal al mesero
                    }

                # Obtén el id de la sucursal del pedido
                id_sucursal_pedido = None
                nombre_sucursal_pedido = None
                if pedido.id_Sucursal:
                    id_sucursal_pedido = pedido.id_Sucursal.id_sucursal
                    nombre_sucursal_pedido = pedido.id_Sucursal.snombre
                elif mesero_info and 'id_sucursal' in mesero_info:
                    id_sucursal_pedido = mesero_info['id_sucursal']
                    nombre_sucursal_pedido = sucursales_dict[id_sucursal_pedido].snombre

                pedido_data = {
                    'id_pedido': pedido.id_pedido,
                    'id_sucursal': id_sucursal_pedido,
                    'nombre_sucursal': nombre_sucursal_pedido,
                    'cliente': {
                        'id_cliente': pedido.id_cliente.id_cliente,
                        'crazon_social': pedido.id_cliente.crazon_social,
                        'ctelefono': pedido.id_cliente.ctelefono,
                        'snombre': pedido.id_cliente.snombre,
                        'capellido': pedido.id_cliente.capellido,
                        'ccorreo_electronico': pedido.id_cliente.ccorreo_electronico,
                    },
                    'mesero': mesero_info,
                    'precio': pedido.precio,
                    'tipo_de_pedido': pedido.tipo_de_pedido,
                    'metodo_de_pago': pedido.metodo_de_pago,
                    'puntos': pedido.puntos,
                    'fecha_pedido': pedido.fecha_pedido,
                    'fecha_entrega': pedido.fecha_entrega,
                    'estado_del_pedido': pedido.estado_del_pedido,
                    'observacion_del_cliente': pedido.observacion_del_cliente,
                    'detalle_pedido': detalle_pedido_data,
                }

                data.append(pedido_data)

            return JsonResponse({'pedidos': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class ListaPedidosIdSucuReportes(View):
    def get(self, request, id_sucursal, *args, **kwargs):
        try:
            # Obtén la lista de pedidos con información del cliente, detalle del pedido y mesero
            pedidos_mesero = Pedidos.objects.filter(
                estado_pago='Pagado',
                factura__id_mesero__id_sucursal=id_sucursal
            )

            pedidos_pedido = Pedidos.objects.filter(
                estado_pago='Pagado',
                id_Sucursal__id_sucursal=id_sucursal
            )

            # Formatea los datos
            data = []
            
            # Obtener el objeto Sucursal
            sucursal = Sucursales.objects.get(id_sucursal=id_sucursal)
            nombre_sucursal = sucursal.snombre

            for pedido in pedidos_mesero:
                detalle_pedido_data = []
                for detalle_pedido in pedido.detallepedidos_set.all():
                    producto_data = {
                        'id_producto': detalle_pedido.id_producto.id_producto,
                        'nombreproducto': detalle_pedido.id_producto.nombreproducto,
                        'cantidad': detalle_pedido.cantidad,
                        'precio_unitario': detalle_pedido.precio_unitario,
                        'impuesto': detalle_pedido.impuesto,
                        'descuento': detalle_pedido.descuento,
                    }
                    detalle_pedido_data.append(producto_data)

                # Obtén el ID del mesero asociado al pedido
                factura = pedido.factura_set.first()
                id_mesero = factura.id_mesero.id_mesero if factura and factura.id_mesero else None
                mesero_info = None
                if id_mesero:
                    mesero = Meseros.objects.get(id_mesero=id_mesero)
                    mesero_info = {
                        'id_mesero': mesero.id_mesero,
                        'nombre': mesero.nombre,
                        'apellido': mesero.apellido,
                        'telefono': mesero.telefono,
                        'fecha_registro': mesero.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
                        'sestado': mesero.sestado,
                        'id_sucursal': mesero.id_sucursal.id_sucursal,
                    }

                pedido_data = {
                    'id_pedido': pedido.id_pedido,
                    'id_sucursal': id_sucursal,
                    'nombre_sucursal': nombre_sucursal,
                    'cliente': {
                        'id_cliente': pedido.id_cliente.id_cliente,
                        'crazon_social': pedido.id_cliente.crazon_social,
                        'ctelefono': pedido.id_cliente.ctelefono,
                        'snombre': pedido.id_cliente.snombre,
                        'capellido': pedido.id_cliente.capellido,
                        'ccorreo_electronico': pedido.id_cliente.ccorreo_electronico,
                    },
                    'mesero': mesero_info,
                    'precio': pedido.precio,
                    'tipo_de_pedido': pedido.tipo_de_pedido,
                    'metodo_de_pago': pedido.metodo_de_pago,
                    'puntos': pedido.puntos,
                    'fecha_pedido': pedido.fecha_pedido,
                    'fecha_entrega': pedido.fecha_entrega,
                    'estado_del_pedido': pedido.estado_del_pedido,
                    'observacion_del_cliente': pedido.observacion_del_cliente,
                    'detalle_pedido': detalle_pedido_data,
                }

                data.append(pedido_data)

            for pedido in pedidos_pedido:
                detalle_pedido_data = []
                for detalle_pedido in pedido.detallepedidos_set.all():
                    producto_data = {
                        'id_producto': detalle_pedido.id_producto.id_producto,
                        'nombreproducto': detalle_pedido.id_producto.nombreproducto,
                        'cantidad': detalle_pedido.cantidad,
                        'precio_unitario': detalle_pedido.precio_unitario,
                        'impuesto': detalle_pedido.impuesto,
                        'descuento': detalle_pedido.descuento,
                    }
                    detalle_pedido_data.append(producto_data)

                pedido_data = {
                    'id_pedido': pedido.id_pedido,
                    'id_sucursal': id_sucursal,
                    'nombre_sucursal': nombre_sucursal,
                    'cliente': {
                        'id_cliente': pedido.id_cliente.id_cliente,
                        'crazon_social': pedido.id_cliente.crazon_social,
                        'ctelefono': pedido.id_cliente.ctelefono,
                        'snombre': pedido.id_cliente.snombre,
                        'capellido': pedido.id_cliente.capellido,
                        'ccorreo_electronico': pedido.id_cliente.ccorreo_electronico,
                    },
                    'mesero': None,
                    'precio': pedido.precio,
                    'tipo_de_pedido': pedido.tipo_de_pedido,
                    'metodo_de_pago': pedido.metodo_de_pago,
                    'puntos': pedido.puntos,
                    'fecha_pedido': pedido.fecha_pedido,
                    'fecha_entrega': pedido.fecha_entrega,
                    'estado_del_pedido': pedido.estado_del_pedido,
                    'observacion_del_cliente': pedido.observacion_del_cliente,
                    'detalle_pedido': detalle_pedido_data,
                }

                data.append(pedido_data)

            return JsonResponse({'pedidos': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
class ListaPedidosProductoReportes(View):
    def get(self, request, *args, **kwargs):
        try:
            # Obtén los parámetros de la solicitud (si los hay)
            id_producto = request.GET.get('id_producto')
            
            # Obtén la lista de pedidos con información del cliente, detalle del pedido y mesero
            pedidos = Pedidos.objects.filter(estado_pago='Pagado')
            
            # Filtrar pedidos por producto si se proporciona un id_producto
            if id_producto:
                pedidos = pedidos.filter(detallepedidos__id_producto=id_producto)
            
            # Obtén la lista de meseros
            meseros = Meseros.objects.all()
            meseros_dict = {mesero.id_mesero: mesero for mesero in meseros}
            
            # Obtén la lista de sucursales
            sucursales = Sucursales.objects.all()
            sucursales_dict = {sucursal.id_sucursal: sucursal for sucursal in sucursales}
            
            # Formatea los datos
            data = []
            for pedido in pedidos:
                detalle_pedido_data = []
                for detalle_pedido in pedido.detallepedidos_set.all():
                    producto_data = {
                        'id_producto': detalle_pedido.id_producto.id_producto,
                        'nombreproducto': detalle_pedido.id_producto.nombreproducto,
                        'cantidad': detalle_pedido.cantidad,
                        'precio_unitario': detalle_pedido.precio_unitario,
                        'impuesto': detalle_pedido.impuesto,
                        'descuento': detalle_pedido.descuento,
                    }
                    detalle_pedido_data.append(producto_data)
                
                # Obtén el ID del mesero asociado al pedido (si existe)
                factura = pedido.factura_set.first()
                id_mesero = factura.id_mesero.id_mesero if factura and factura.id_mesero else None
                mesero_info = None
                if id_mesero:
                    mesero = meseros_dict[id_mesero]
                    mesero_info = {
                        'id_mesero': mesero.id_mesero,
                        'nombre': mesero.nombre,
                        'apellido': mesero.apellido,
                        'telefono': mesero.telefono,
                        'fecha_registro': mesero.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
                        'sestado': mesero.sestado,
                        'id_sucursal': mesero.id_sucursal.id_sucursal,  # Agregar el ID de la sucursal al mesero
                        'nombre_sucursal': mesero.id_sucursal.snombre,  # Agregar el nombre de la sucursal al mesero
                    }
                
                # Obtén el id de la sucursal del pedido
                id_sucursal_pedido = None
                nombre_sucursal_pedido = None
                if pedido.id_Sucursal:
                    id_sucursal_pedido = pedido.id_Sucursal.id_sucursal
                    nombre_sucursal_pedido = pedido.id_Sucursal.snombre
                elif mesero_info and 'id_sucursal' in mesero_info:
                    id_sucursal_pedido = mesero_info['id_sucursal']
                    nombre_sucursal_pedido = sucursales_dict[id_sucursal_pedido].snombre
                
                pedido_data = {
                    'id_pedido': pedido.id_pedido,
                    'id_sucursal': id_sucursal_pedido,
                    'nombre_sucursal': nombre_sucursal_pedido,
                    'cliente': {
                        'id_cliente': pedido.id_cliente.id_cliente,
                        'crazon_social': pedido.id_cliente.crazon_social,
                        'ctelefono': pedido.id_cliente.ctelefono,
                        'snombre': pedido.id_cliente.snombre,
                        'capellido': pedido.id_cliente.capellido,
                        'ccorreo_electronico': pedido.id_cliente.ccorreo_electronico,
                    },
                    'mesero': mesero_info,
                    'precio': pedido.precio,
                    'tipo_de_pedido': pedido.tipo_de_pedido,
                    'metodo_de_pago': pedido.metodo_de_pago,
                    'puntos': pedido.puntos,
                    'fecha_pedido': pedido.fecha_pedido,
                    'fecha_entrega': pedido.fecha_entrega,
                    'estado_del_pedido': pedido.estado_del_pedido,
                    'observacion_del_cliente': pedido.observacion_del_cliente,
                    'detalle_pedido': detalle_pedido_data,
                }
                
                data.append(pedido_data)
            
            return JsonResponse({'pedidos': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class ListaPedidosIdProductoReportes(View):
    def get(self, request, id_producto, *args, **kwargs):
        try:
            # Obtén la lista de pedidos con información del cliente, detalle del pedido y mesero
            pedidos = Pedidos.objects.filter(
                estado_pago='Pagado',
                detallepedidos__id_producto=id_producto
            )

            # Obtén la lista de meseros
            meseros = Meseros.objects.all()
            meseros_dict = {mesero.id_mesero: mesero for mesero in meseros}

            # Obtén la lista de sucursales
            sucursales = Sucursales.objects.all()
            sucursales_dict = {sucursal.id_sucursal: sucursal for sucursal in sucursales}

            # Formatea los datos
            data = []
            for pedido in pedidos:
                detalle_pedido_data = []
                for detalle_pedido in pedido.detallepedidos_set.all():
                    producto_data = {
                        'id_producto': detalle_pedido.id_producto.id_producto,
                        'nombreproducto': detalle_pedido.id_producto.nombreproducto,
                        'cantidad': detalle_pedido.cantidad,
                        'precio_unitario': detalle_pedido.precio_unitario,
                        'impuesto': detalle_pedido.impuesto,
                        'descuento': detalle_pedido.descuento,
                    }
                    detalle_pedido_data.append(producto_data)

                # Obtén el ID del mesero asociado al pedido (si existe)
                factura = pedido.factura_set.first()
                id_mesero = factura.id_mesero.id_mesero if factura and factura.id_mesero else None
                mesero_info = None
                if id_mesero:
                    mesero = meseros_dict[id_mesero]
                    mesero_info = {
                        'id_mesero': mesero.id_mesero,
                        'nombre': mesero.nombre,
                        'apellido': mesero.apellido,
                        'telefono': mesero.telefono,
                        'fecha_registro': mesero.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
                        'sestado': mesero.sestado,
                        'id_sucursal': mesero.id_sucursal.id_sucursal,  # Agregar el ID de la sucursal al mesero
                        'nombre_sucursal': mesero.id_sucursal.snombre,  # Agregar el nombre de la sucursal al mesero
                    }

                # Obtén el id de la sucursal del pedido
                id_sucursal_pedido = None
                nombre_sucursal_pedido = None
                if pedido.id_Sucursal:
                    id_sucursal_pedido = pedido.id_Sucursal.id_sucursal
                    nombre_sucursal_pedido = pedido.id_Sucursal.snombre
                elif mesero_info and 'id_sucursal' in mesero_info:
                    id_sucursal_pedido = mesero_info['id_sucursal']
                    nombre_sucursal_pedido = sucursales_dict[id_sucursal_pedido].snombre

                pedido_data = {
                    'id_pedido': pedido.id_pedido,
                    'id_sucursal': id_sucursal_pedido,
                    'nombre_sucursal': nombre_sucursal_pedido,
                    'cliente': {
                        'id_cliente': pedido.id_cliente.id_cliente,
                        'crazon_social': pedido.id_cliente.crazon_social,
                        'ctelefono': pedido.id_cliente.ctelefono,
                        'snombre': pedido.id_cliente.snombre,
                        'capellido': pedido.id_cliente.capellido,
                        'ccorreo_electronico': pedido.id_cliente.ccorreo_electronico,
                    },
                    'mesero': mesero_info,
                    'precio': pedido.precio,
                    'tipo_de_pedido': pedido.tipo_de_pedido,
                    'metodo_de_pago': pedido.metodo_de_pago,
                    'puntos': pedido.puntos,
                    'fecha_pedido': pedido.fecha_pedido,
                    'fecha_entrega': pedido.fecha_entrega,
                    'estado_del_pedido': pedido.estado_del_pedido,
                    'observacion_del_cliente': pedido.observacion_del_cliente,
                    'detalle_pedido': detalle_pedido_data,
                }

                data.append(pedido_data)

            return JsonResponse({'pedidos': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
class ListaPedidosTipoPReportes(View):
    def get(self, request, *args, **kwargs):
        try:

            productos = Producto.objects.all()

            # Lista de IDs de todos los productos
            ids_productos = productos.values_list('id_producto', flat=True)

            # Obtén la lista de pedidos con información del cliente, detalle del pedido y mesero
            pedidos = Pedidos.objects.filter(
                estado_pago='Pagado',
                detallepedidos__id_producto__in=ids_productos
            ).distinct()

            # Obtén la lista de meseros
            meseros = Meseros.objects.all()
            meseros_dict = {mesero.id_mesero: mesero for mesero in meseros}

            # Obtén la lista de sucursales
            sucursales = Sucursales.objects.all()
            sucursales_dict = {sucursal.id_sucursal: sucursal for sucursal in sucursales}

            # Formatea los datos
            data = {
                'pedidos': [],
            }
            for pedido in pedidos:
                detalle_pedido_data = []
                detalle_pedidos_procesados = set()  # Mantener un conjunto de IDs de detalle de pedidos procesados
                for detalle_pedido in pedido.detallepedidos_set.all():
                    # Evitar duplicados de pedidos que tienen múltiples productos
                    if detalle_pedido.id_producto.id_producto not in detalle_pedidos_procesados:
                        producto_data = {
                            'id_producto': detalle_pedido.id_producto.id_producto,
                            'nombreproducto': detalle_pedido.id_producto.nombreproducto,
                            'cantidad': detalle_pedido.cantidad,
                            'precio_unitario': detalle_pedido.precio_unitario,
                            'impuesto': detalle_pedido.impuesto,
                            'descuento': detalle_pedido.descuento,
                        }
                        detalle_pedido_data.append(producto_data)
                        detalle_pedidos_procesados.add(detalle_pedido.id_producto.id_producto)

                # Obtén el ID del mesero asociado al pedido (si existe)
                factura = pedido.factura_set.first()
                id_mesero = factura.id_mesero.id_mesero if factura and factura.id_mesero else None
                mesero_info = None
                if id_mesero:
                    mesero = meseros_dict[id_mesero]
                    mesero_info = {
                        'id_mesero': mesero.id_mesero,
                        'nombre': mesero.nombre,
                        'apellido': mesero.apellido,
                        'telefono': mesero.telefono,
                        'fecha_registro': mesero.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
                        'sestado': mesero.sestado,
                        'id_sucursal': mesero.id_sucursal.id_sucursal,  # Agregar el ID de la sucursal al mesero
                        'nombre_sucursal': mesero.id_sucursal.snombre,  # Agregar el nombre de la sucursal al mesero
                    }

                # Obtén el id de la sucursal del pedido
                id_sucursal_pedido = None
                nombre_sucursal_pedido = None
                if pedido.id_Sucursal:
                    id_sucursal_pedido = pedido.id_Sucursal.id_sucursal
                    nombre_sucursal_pedido = pedido.id_Sucursal.snombre
                elif mesero_info and 'id_sucursal' in mesero_info:
                    id_sucursal_pedido = mesero_info['id_sucursal']
                    nombre_sucursal_pedido = sucursales_dict[id_sucursal_pedido].snombre

                pedido_data = {
                    'id_pedido': pedido.id_pedido,
                    'id_tipoproducto': detalle_pedido.id_producto.id_categoria.id_tipoproducto.id_tipoproducto,
                    'nombretp': detalle_pedido.id_producto.id_categoria.id_tipoproducto.tpnombre,
                    'id_sucursal': id_sucursal_pedido,
                    'nombre_sucursal': nombre_sucursal_pedido,
                    'cliente': {
                        'id_cliente': pedido.id_cliente.id_cliente,
                        'crazon_social': pedido.id_cliente.crazon_social,
                        'ctelefono': pedido.id_cliente.ctelefono,
                        'snombre': pedido.id_cliente.snombre,
                        'capellido': pedido.id_cliente.capellido,
                        'ccorreo_electronico': pedido.id_cliente.ccorreo_electronico,
                    },
                    'mesero': mesero_info,
                    'precio': pedido.precio,
                    'tipo_de_pedido': pedido.tipo_de_pedido,
                    'metodo_de_pago': pedido.metodo_de_pago,
                    'puntos': pedido.puntos,
                    'fecha_pedido': pedido.fecha_pedido,
                    'fecha_entrega': pedido.fecha_entrega,
                    'estado_del_pedido': pedido.estado_del_pedido,
                    'observacion_del_cliente': pedido.observacion_del_cliente,
                    'detalle_pedido': detalle_pedido_data,
                }

                data['pedidos'].append(pedido_data)

            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class ListaTipos(View):
    def get(self, request, id_tipoproducto, *args, **kwargs):
        try:
            # Obtén la lista de productos que pertenecen al tipo de producto dado
            productos = Producto.objects.filter(
                id_categoria__id_tipoproducto=id_tipoproducto
            )

            # Lista de IDs de productos que pertenecen al tipo de producto dado
            ids_productos = productos.values_list('id_producto', flat=True)

             # Obtén la lista de pedidos con información del cliente, detalle del pedido y mesero
            pedidos = Pedidos.objects.filter(
                estado_pago='Pagado',
                detallepedidos__id_producto__in=ids_productos
            ).distinct()

            # Obtén la lista de meseros
            meseros = Meseros.objects.all()
            meseros_dict = {mesero.id_mesero: mesero for mesero in meseros}

            # Obtén la lista de sucursales
            sucursales = Sucursales.objects.all()
            sucursales_dict = {sucursal.id_sucursal: sucursal for sucursal in sucursales}

            # Formatea los datos
            data = {
                'id_tipoproducto': id_tipoproducto,
                'pedidos': [],
            }
            for pedido in pedidos:
                detalle_pedido_data = []
                detalle_pedidos_procesados = set()  # Mantener un conjunto de IDs de detalle de pedidos procesados
                for detalle_pedido in pedido.detallepedidos_set.all():
                    # Evitar duplicados de pedidos que tienen múltiples productos
                    if detalle_pedido.id_producto.id_producto not in detalle_pedidos_procesados:
                        producto_data = {
                            'id_producto': detalle_pedido.id_producto.id_producto,
                            'nombreproducto': detalle_pedido.id_producto.nombreproducto,
                            'cantidad': detalle_pedido.cantidad,
                            'precio_unitario': detalle_pedido.precio_unitario,
                            'impuesto': detalle_pedido.impuesto,
                            'descuento': detalle_pedido.descuento,
                        }
                        detalle_pedido_data.append(producto_data)
                        detalle_pedidos_procesados.add(detalle_pedido.id_producto.id_producto)

                # Obtén el ID del mesero asociado al pedido (si existe)
                factura = pedido.factura_set.first()
                id_mesero = factura.id_mesero.id_mesero if factura and factura.id_mesero else None
                mesero_info = None
                if id_mesero:
                    mesero = meseros_dict[id_mesero]
                    mesero_info = {
                        'id_mesero': mesero.id_mesero,
                        'nombre': mesero.nombre,
                        'apellido': mesero.apellido,
                        'telefono': mesero.telefono,
                        'fecha_registro': mesero.fecha_registro.strftime('%Y-%m-%d %H:%M:%S'),
                        'sestado': mesero.sestado,
                        'id_sucursal': mesero.id_sucursal.id_sucursal,  # Agregar el ID de la sucursal al mesero
                        'nombre_sucursal': mesero.id_sucursal.snombre,  # Agregar el nombre de la sucursal al mesero
                    }

                # Obtén el id de la sucursal del pedido
                id_sucursal_pedido = None
                nombre_sucursal_pedido = None
                if pedido.id_Sucursal:
                    id_sucursal_pedido = pedido.id_Sucursal.id_sucursal
                    nombre_sucursal_pedido = pedido.id_Sucursal.snombre
                elif mesero_info and 'id_sucursal' in mesero_info:
                    id_sucursal_pedido = mesero_info['id_sucursal']
                    nombre_sucursal_pedido = sucursales_dict[id_sucursal_pedido].snombre

                pedido_data = {
                    'id_pedido': pedido.id_pedido,
                    'id_tipoproducto': id_tipoproducto,
                    'nombretp': detalle_pedido.id_producto.id_categoria.id_tipoproducto.tpnombre,
                    'id_sucursal': id_sucursal_pedido,
                    'nombre_sucursal': nombre_sucursal_pedido,
                    'cliente': {
                        'id_cliente': pedido.id_cliente.id_cliente,
                        'crazon_social': pedido.id_cliente.crazon_social,
                        'ctelefono': pedido.id_cliente.ctelefono,
                        'snombre': pedido.id_cliente.snombre,
                        'capellido': pedido.id_cliente.capellido,
                        'ccorreo_electronico': pedido.id_cliente.ccorreo_electronico,
                    },
                    'mesero': mesero_info,
                    'precio': pedido.precio,
                    'tipo_de_pedido': pedido.tipo_de_pedido,
                    'metodo_de_pago': pedido.metodo_de_pago,
                    'puntos': pedido.puntos,
                    'fecha_pedido': pedido.fecha_pedido,
                    'fecha_entrega': pedido.fecha_entrega,
                    'estado_del_pedido': pedido.estado_del_pedido,
                    'observacion_del_cliente': pedido.observacion_del_cliente,
                    'detalle_pedido': detalle_pedido_data,
                }

                data['pedidos'].append(pedido_data)

            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)