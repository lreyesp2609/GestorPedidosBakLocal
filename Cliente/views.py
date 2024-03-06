import base64
import re
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from Ubicaciones.models import Ubicaciones
from Mesero.models import *
from Producto.models import Producto
from django.views.decorators.csrf import csrf_exempt
from PIL import Image, UnidentifiedImageError
from django.utils.decorators import method_decorator
from django.views import View
from datetime import datetime
from django.db import transaction
import json
from decimal import Decimal, InvalidOperation
from pagos.models import PagosTransferencia, PagosEfectivo,PagosPasarela
from Login.models import Cuenta
import traceback

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
            precio = request.POST.get('precio', 0)
            print(precio)
            fecha_pedido = datetime.now()
            tipo_de_pedido = request.POST.get('tipo_de_pedido')
            metodo_de_pago = request.POST.get('metodo_de_pago')
            puntos = request.POST.get('puntos', 0)
            estado_del_pedido = request.POST.get('estado_del_pedido', 'O')
            sucursal = request.POST.get('id_sucursal')
            latitud = request.POST.get('latitud')
            longitud = request.POST.get('longitud')
            estado_pago = request.POST.get('estado_pago', 'En revisión')
            imagen_archivo = request.FILES.get('imagen')
            hora = (request.POST.get('fecha_hora'))
            if sucursal:
                sucursal=Sucursales.objects.first().id_sucursal
            ubicacion=None
            if latitud:
                ubicacion= Ubicaciones.objects.create(
                    latitud=latitud,
                    longitud=longitud,
                    sestado=1
                )
            image_64_encode = None
            if imagen_archivo:
                try:
                    image_read = imagen_archivo.read()
                    image_64_encode = base64.b64encode(image_read)
                    image_encoded = image_64_encode.decode('utf-8')
                except UnidentifiedImageError as img_error:
                    return JsonResponse({'error': f"Error al procesar imagen: {str(img_error)}"}, status=400)

            detalles_pedido_raw = request.POST.get('detalles_pedido', '{}')
            detalles_pedido = json.loads(detalles_pedido_raw)

            total_precio_pedido = Decimal(0)
            total_descuento = Decimal(0)
            detalles_factura = []
            if hora:
                hora=int(hora)
                minuto = int(request.POST.get('fecha_minutos'))
                fecha_hora_entrega = fecha_pedido.replace(hour=hora, minute=minuto, second=0, microsecond=0)
                fecha_hora_entrega_formato_correcto = fecha_hora_entrega.strftime('%Y-%m-%d %H:%M:%S')
                fecha_pedido=fecha_hora_entrega_formato_correcto
            nuevo_pedido = Pedidos.objects.create(
                id_cliente=id_cliente,
                precio=precio,
                tipo_de_pedido=tipo_de_pedido,
                metodo_de_pago=metodo_de_pago,
                fecha_pedido=fecha_pedido,
                puntos=puntos,
                estado_del_pedido=estado_del_pedido,
                estado_pago=estado_pago,
                imagen=image_64_encode,
                id_Ubicacion= ubicacion,
                id_Sucursal= Sucursales.objects.get(id_sucursal=sucursal)
            )

            for detalle_pedido_data in detalles_pedido['detalles_pedido']:
                id_producto = detalle_pedido_data.get('id_producto')
                producto_asociado = Producto.objects.get(id_producto=id_producto)
                cantidad = Decimal(detalle_pedido_data.get('cantidad_pedido'))
                precio_unitario = Decimal(detalle_pedido_data.get('costo_unitario'))
                # Impuesto establecido en 0 para evitar que se calcule
                impuesto = Decimal(0)
                descuento = Decimal(detalle_pedido_data.get('descuento', 0))

                precio_total_detalle = (precio_unitario * cantidad) - descuento
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
                a_pagar=total_a_pagar,
                estado='P',
                codigo_autorizacion=Codigoautorizacion.obtener_codigo_autorizacion_valido(),
                fecha_emision=datetime.now(),
            )

            for detalle in detalles_factura:
                id_producto = detalle.get('id_producto')
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
            traceback.print_exc()
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

def ver_factura_cliente(request, id_cuenta, id_pedido, **kwargs):
    print("ID de cuenta recibido:", id_cuenta)
    print("ID de pedido recibido:", id_pedido)
    try:
        cliente = get_object_or_404(Clientes, id_cuenta=id_cuenta)
        factura = Factura.objects.get(id_pedido_id=id_pedido)
        
        # Verificar si el pedido pertenece al cliente dado
        pedido = Pedidos.objects.get(pk=id_pedido)
        if pedido.id_cliente_id != cliente.id_cliente:
            return JsonResponse({'error': 'El pedido no pertenece al cliente dado'}, status=404)
        
        detalles_factura = DetalleFactura.objects.filter(id_factura_id=factura.id_factura).values()

        detalles_factura_list = list(detalles_factura)

        # Obtener información del pedido
        tipo_de_pedido = pedido.tipo_de_pedido
        metodo_de_pago = pedido.metodo_de_pago
        detalles_factura_list = list(detalles_factura)
        id_cliente = factura.id_cliente_id

        # Obtener la información de la factura
        codigo_autorizacion_sri = factura.codigo_autorizacion
        codigo_autorizacion_obj = Codigoautorizacion.objects.get(codigo_autorizacion=codigo_autorizacion_sri)
        fecha_autorizacion = codigo_autorizacion_obj.fecha_autorizacion
        fecha_vencimiento = codigo_autorizacion_obj.fecha_vencimiento

        # Obtener la numeración desde el modelo Codigosri
        numeracion = f"{factura.numero_factura_desde}-{factura.numero_factura_hasta}"

        # Obtener el punto de facturación asociado a la factura
        punto_facturacion = Puntofacturacion.objects.get(id_puntofacturacion=factura.id_punto_facturacion_id)
        mesero = Meseros.objects.get(id_mesero=punto_facturacion.id_mesero.id_mesero)  # Obtener el objeto del mesero

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
            'nombre_mesero': mesero.nombre,  # Agregar nombre del mesero
            'apellido_mesero': mesero.apellido,  # Agregar apellido del mesero
            'ruc': punto_facturacion.ruc,  # Agregar RUC del punto de facturación
        }
        return JsonResponse(factura_data)
    except Factura.DoesNotExist:
        traceback.print_exc()
        return JsonResponse({'error': 'La factura no existe'}, status=404)
    except Clientes.DoesNotExist:
        traceback.print_exc()
        return JsonResponse({'error': 'El cliente no existe'}, status=404)



class obtenerPedidos(View):
    def get(self, request, *args, **kwargs):
        try:
            id_usuario = kwargs.get('id_cuenta')

            cliente = get_object_or_404(Clientes, id_cuenta=id_usuario)
            
            # Obtener todos los pedidos del cliente
            pedidos_cliente = Pedidos.objects.filter(id_cliente=cliente)

            # Crear una lista para almacenar los datos de cada pedido
            lista_pedidos = []

            for pedido in pedidos_cliente:

                pedido_data = {
                    'id_pedido': pedido.id_pedido,
                    'nombre_usuario': cliente.snombre,
                    'apellido_usuario': cliente.capellido,
                    'idcliente': cliente.id_cliente,
                    'Total': pedido.precio,
                    'Pago':pedido.estado_pago,
                    'estado_del_pedido': pedido.estado_del_pedido,
                    'fecha_pedido': pedido.fecha_pedido,
                }

                lista_pedidos.append(pedido_data)

            return JsonResponse({'Pedidos': lista_pedidos})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
class obtenerPedidos2(View):
    def get(self, request, *args, **kwargs):
        try:
            pedidos = Pedidos.objects.all()

            lista_pedidos = []

            for pedido in pedidos:
                id_cliente = pedido.id_cliente.id_cuenta
                

                cliente = get_object_or_404(Clientes, id_cuenta=id_cliente)
                imagen_base64 = None
                if pedido.imagen:
                    try:
                        byteImg = base64.b64decode(pedido.imagen)
                        imagen_base64 = base64.b64encode(byteImg).decode('utf-8')
                    except Exception as img_error:
                        print(f"Error al procesar imagen: {str(img_error)}")
                pedido_data = {
                    'nombre_usuario': cliente.snombre,
                    'apellido_usuario': cliente.capellido,
                    'idcliente': cliente.id_cliente,
                    'id_pedido':pedido.id_pedido,
                    'Total': pedido.precio,
                    'metodo_de_pago':pedido.metodo_de_pago,
                    'Pago': pedido.estado_pago,
                    'estado_del_pedido': pedido.estado_del_pedido,
                    'fecha_pedido': pedido.fecha_pedido,
                    'imagen': imagen_base64 
                }


                lista_pedidos.append(pedido_data)

            return JsonResponse({'Pedidos': lista_pedidos})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class CambiarEstadoPedidos(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            id_pedido = kwargs.get('id_pedido')

            # Obtener el objeto Pedidos que se desea actualizar
            pedido = Pedidos.objects.get(id_pedido=id_pedido)
            

            # Acceder a los datos directamente desde request.POST y request.FILES
            estado_del_pedido = request.POST.get('estado_del_pedido')
            dzero = Decimal(str(pedido.precio.replace(',', '.').replace('€', '').replace('$', '')))
            precio_str = request.POST.get('precio', dzero)
            precio=  precio_str if precio_str else dzero
           
            # Actualizar los campos necesarios
            pedido.estado_del_pedido = estado_del_pedido
          
            pedido.precio = precio
            # Puedes hacer lo mismo para otros campos que desees actualizar

            # Guardar los cambios en la base de datos
            pedido.save()

            return JsonResponse({'success': True, 'message': 'Pedido actualizado con éxito.'})
        except Exception as e:
            # Si ocurre un error, devolver un mensaje de error
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
        
@method_decorator(csrf_exempt, name='dispatch')
class CambiarEstadoPagos(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                id_pedido = kwargs.get('id_pedido')

                # Obtener el objeto Pedidos que se desea actualizar
                pedido = Pedidos.objects.get(id_pedido=id_pedido)
                idcuenta= request.POST.get('id_cuenta')
                usuario= Cuenta.objects.get(id_cuenta=idcuenta)

                # Acceder a los datos directamente desde request.POST y request.FILES
                estado_pago = request.POST.get('estado_pago')
            
                # Actualizar los campos necesarios
                pedido.estado_pago = estado_pago
                
                pedido.save()
                if pedido.metodo_de_pago=='T':
                    PagosTrans=PagosTransferencia.objects.create(
                        id_pedido = pedido,
                        estado = 'E',
                        cantidad = pedido.precio,
                        hora_de_pago = pedido.fecha_pedido,
                        id_cuentacobrador = usuario,
                        comprobante = pedido.imagen,
                        hora_confirmacion_pago = datetime.now()
                    )
                if pedido.metodo_de_pago=='E':
                    PagosEfec=PagosEfectivo.objects.create(
                        estado = 'X',
                        cantidad = pedido.precio,
                        cantidadentregada = pedido.precio,
                        cambioeentregado = 0,
                        hora_de_pago = datetime.now(),
                        id_cuentacobrador = usuario,
                        id_pedido = pedido
                    )
                if pedido.metodo_de_pago=='X':
                    PagosPas=PagosPasarela.objects.create(
                        id_pedido = pedido,
                        estado = 'E',
                        cantidad = pedido.precio,
                        hora_de_pago = pedido.fecha_pedido,
                        codigo_unico = '102'
                    )

                return JsonResponse({'success': True, 'message': 'Pago actualizado con éxito.'})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
def verificar_pedido_validado(request, id_factura):
    try:
        factura = Factura.objects.get(id_factura=id_factura)
        pedido = factura.id_pedido
        estado_pago = pedido.estado_pago
        numero_factura = factura.id_factura
        
        if estado_pago == 'En revisión':
            mensaje = f'El pedido asociado a la factura {numero_factura} todavía se encuentra en revisión.'
        elif estado_pago == 'Pagado':
            mensaje = f'El pedido asociado a la factura {numero_factura} se encuentra pagado.'
        elif estado_pago == 'Denegado':
            mensaje = f'El pedido asociado a la factura {numero_factura} se denegó.'
        else:
            mensaje = 'Estado de pago no reconocido'
        
        return JsonResponse({'message': mensaje, 'status': estado_pago}, status=200)
    except Factura.DoesNotExist:
        return JsonResponse({'error': 'La factura no existe'}, status=404)
    except Pedidos.DoesNotExist:
        return JsonResponse({'error': 'El pedido asociado no existe'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

