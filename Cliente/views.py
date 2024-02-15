from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Ubicaciones.models import Ubicaciones
from Mesero.models import *
from Producto.models import Producto
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from datetime import datetime
from django.db import transaction
import json
from decimal import Decimal

@method_decorator(csrf_exempt, name='dispatch')
class ActualizarClienteView(View):
    @login_required
    def post(self, request, *args, **kwargs):
        try:
            user = request.user  # Obtener el usuario autenticado

            # Obtener los datos del cuerpo de la solicitud
            data = json.loads(request.body)
            
            # Actualizar los campos en el modelo Clientes asociado al usuario
            user.clientes.crazon_social = data.get('crazon_social', user.clientes.crazon_social)
            user.clientes.snombre = data.get('snombre', user.clientes.snombre)
            user.clientes.capellido = data.get('capellido', user.clientes.capellido)
            user.clientes.ruc_cedula = data.get('ruc_cedula', user.clientes.ruc_cedula)
            user.clientes.ccorreo_electronico = data.get('ccorreo_electronico', user.clientes.ccorreo_electronico)
            user.clientes.ubicacion = data.get('ubicacion', user.clientes.ubicacion)
            
            # Guardar los cambios
            user.clientes.save()

            return JsonResponse({'mensaje': 'Datos del cliente actualizados correctamente'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class EditarCliente(View):
    def post(self, request, id_cliente, *args, **kwargs):
        try:
            # Obtener el cliente específico
            cliente = get_object_or_404(Clientes, id_cliente=id_cliente)

            # Obtener los datos del cuerpo de la solicitud
            data = json.loads(request.body)

            # Actualizar los campos en el modelo Clientes
            cliente.crazon_social = data.get('crazon_social', cliente.crazon_social)
            cliente.snombre = data.get('snombre', cliente.snombre)
            cliente.capellido = data.get('capellido', cliente.capellido)
            cliente.ruc_cedula = data.get('ruc_cedula', cliente.ruc_cedula)
            cliente.ccorreo_electronico = data.get('ccorreo_electronico', cliente.ccorreo_electronico)
            cliente.ubicacion = data.get('ubicacion', cliente.ubicacion)
            cliente.ctelefono = data.get('ctelefono', cliente.ctelefono)
            cliente.tipocliente = data.get('tipocliente', cliente.tipocliente)
            cliente.cpuntos = data.get('cpuntos', cliente.cpuntos)

            # Guardar los cambios
            cliente.save()

            return JsonResponse({'mensaje': 'Datos del cliente actualizados correctamente'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
from Cliente.models import Clientes

@method_decorator(csrf_exempt, name='dispatch')
class VerClientesView(View):
    def get(self, request, *args, **kwargs):
        try:
            clientes = Clientes.objects.all()

            clientes_data = []
            for cliente in clientes:
                cliente_data = {
                    'id_cliente': cliente.id_cliente,
                    'crazon_social': cliente.crazon_social,
                    'snombre': cliente.snombre,
                    'capellido': cliente.capellido,
                    'ruc_cedula': cliente.ruc_cedula,
                    'ccorreo_electronico': cliente.ccorreo_electronico,
                    'ubicacion': cliente.ubicacion,
                    'ctelefono': cliente.ctelefono,
                    'tipocliente': cliente.tipocliente,
                    'cregistro': cliente.cregistro.strftime('%Y-%m-%d %H:%M:%S'),  # Formato de fecha
                    'cpuntos': str(cliente.cpuntos),  # Convertir a cadena para el formato JSON
                }
                clientes_data.append(cliente_data)

            return JsonResponse({'clientes': clientes_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class EditarCliente(View):
    def post(self, request, id_cliente, *args, **kwargs):
        try:
            # Obtener el cliente específico
            cliente = get_object_or_404(Clientes, id_cliente=id_cliente)

            # Actualizar los campos en el modelo Clientes
            cliente.crazon_social = request.POST.get('crazon_social', cliente.crazon_social)
            cliente.snombre = request.POST.get('snombre', cliente.snombre)
            cliente.capellido = request.POST.get('capellido', cliente.capellido)
            cliente.ruc_cedula = request.POST.get('ruc_cedula', cliente.ruc_cedula)
            cliente.ccorreo_electronico = request.POST.get('ccorreo_electronico', cliente.ccorreo_electronico)
            cliente.ubicacion = request.POST.get('ubicacion', cliente.ubicacion)
            cliente.ctelefono = request.POST.get('ctelefono', cliente.ctelefono)
            cliente.tipocliente = request.POST.get('tipocliente', cliente.tipocliente)
            cliente.cpuntos = request.POST.get('cpuntos', cliente.cpuntos)

            # Guardar los cambios
            cliente.save()

            return JsonResponse({'mensaje': 'Datos del cliente actualizados correctamente'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class RealizarPedidoView(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            id_usuario = kwargs.get('id_cuenta')
            id_cliente = Clientes.objects.get(id_cuenta=id_usuario)

            # Acceder a los datos directamente desde request.POST y request.FILES
            fecha_pedido = datetime.now()
            tipo_de_pedido = request.POST.get('tipo_de_pedido')
            metodo_de_pago = request.POST.get('metodo_de_pago')
            puntos = request.POST.get('puntos', 0)
            estado_del_pedido = request.POST.get('estado_del_pedido', 'O')
            
            detalles_pedido_raw = request.POST.get('detalles_pedido', '{}')
            detalles_pedido = json.loads(detalles_pedido_raw)

            total_precio_pedido = Decimal(0)
            total_descuento = Decimal(0)
            detalles_factura = []

            nuevo_pedido = Pedidos.objects.create(
                id_cliente=id_cliente,
                precio=0,
                tipo_de_pedido=tipo_de_pedido,
                metodo_de_pago=metodo_de_pago,                
                fecha_pedido=fecha_pedido,
                puntos=puntos,
                estado_del_pedido=estado_del_pedido
            )

            for detalle_pedido_data in detalles_pedido['detalles_pedido']:
                id_producto = detalle_pedido_data.get('id_producto')
                producto_asociado = Producto.objects.get(id_producto=id_producto)
                cantidad = Decimal(detalle_pedido_data.get('cantidad_pedido'))
                precio_unitario = Decimal(detalle_pedido_data.get('costo_unitario'))
                impuesto = precio_unitario * Decimal('0.12')  # IVA del 12%
                descuento = Decimal(detalle_pedido_data.get('descuento', 0))

                precio_total_detalle = (precio_unitario + impuesto) * cantidad - descuento
                total_precio_pedido += precio_total_detalle
                total_descuento += descuento

                detalles_factura.append({
                    'id_producto': id_producto,
                    'cantidad': cantidad,
                    'precio_unitario': precio_unitario,
                    'descuento': descuento,
                    'valor': precio_total_detalle
                })

                Detallepedidos.objects.create(
                    id_pedido=nuevo_pedido,
                    id_producto=producto_asociado,
                    cantidad=cantidad,
                    precio_unitario=precio_unitario,
                    impuesto=impuesto,
                    descuento=descuento
                )

            subtotal = total_precio_pedido - total_descuento  # Subtotal = Total - Descuento
            iva = subtotal * Decimal('0.12')  # Calcula el IVA
            total_a_pagar = subtotal + iva  # Total a pagar = Subtotal + IVA

            nuevo_pedido.precio = total_a_pagar  # Actualiza el precio con el total a pagar
            nuevo_pedido.save()

            nueva_factura = Factura.objects.create(
                id_pedido=nuevo_pedido,
                id_cliente=id_cliente,
                total=total_precio_pedido,
                iva=iva,
                descuento=total_descuento,
                subtotal=subtotal,
                a_pagar=total_a_pagar
            )


            for detalle in detalles_factura:
                id_producto = detalle_pedido_data.get('id_producto')
                producto_instance = get_object_or_404(Producto, id_producto=id_producto)
                DetalleFactura.objects.create(
                    id_factura=nueva_factura,
                    id_producto=producto_instance,
                    cantidad=detalle['cantidad'],
                    precio_unitario=detalle['precio_unitario'],
                    descuento=detalle['descuento'],
                    valor=detalle['valor']
                )

            return JsonResponse({'success': True, 'message': 'Pedido realizado con éxito.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
