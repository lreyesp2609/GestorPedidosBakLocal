# views.py
import decimal
from gettext import translation
import json
import traceback
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from Mesero.models import Factura, Meseros, Pedidos, Puntofacturacion
from .models import *
from django.utils.decorators import method_decorator
import re
from decimal import Decimal

@csrf_exempt
def crear_codigosri(request, id_cuenta):
    if request.method == 'POST':
        # Recuperar los datos del formulario POST
        id_administrador = Administrador.objects.get(id_cuenta=id_cuenta)

        numero_factura_desde = request.POST.get('numero_factura_desde')
        numero_factura_hasta = request.POST.get('numero_factura_hasta')

        # Validar el formato de los números de factura
        formato_correcto = re.match(r'^\d{9}$', numero_factura_desde) and re.match(r'^\d{9}$', numero_factura_hasta)
        if not formato_correcto:
            return JsonResponse({'error': 'Los números de factura deben tener exactamente 9 dígitos'}, status=400)

        # Verificar si ya existe un registro en la tabla Codigosri
        if Codigosri.objects.exists():
            # Si existe, actualizar el registro existente en lugar de crear uno nuevo
            codigosri = Codigosri.objects.first()
            codigosri.numero_factura_desde = numero_factura_desde
            codigosri.numero_factura_hasta = numero_factura_hasta
            # Actualizar los campos rango_desde y rango_hasta también
            codigosri.rango_desde = numero_factura_desde
            codigosri.rango_hasta = numero_factura_hasta
            codigosri.save()
        else:
            # Si no existe, crear un nuevo registro en Codigosri
            Codigosri.objects.create(
                id_administrador=id_administrador,
                rango_desde=numero_factura_desde,  # Aseguramos que rango_desde sea igual a numero_factura_desde
                rango_hasta=numero_factura_hasta,  # Aseguramos que rango_hasta sea igual a numero_factura_hasta
                numero_factura_desde=numero_factura_desde,
                numero_factura_hasta=numero_factura_hasta,
            )

        # Retornar una respuesta JSON
        return JsonResponse({'mensaje': 'Codigosri creado o actualizado exitosamente'})
    else:
        # Si la solicitud no es POST, retornar un error
        return JsonResponse({'error': 'Se esperaba una solicitud POST'}, status=400)
@csrf_exempt
def crear_codigoautorizacion(request, id_cuenta):
    if request.method == 'POST':
        # Recuperar los datos del formulario POST
        id_administrador = Administrador.objects.get(id_cuenta=id_cuenta)

        codigo_autorizacion = request.POST.get('codigo_autorizacion')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        fecha_autorizacion = request.POST.get('fecha_autorizacion')
        ruc = request.POST.get('ruc')  # Recuperar el RUC del formulario
        nombre = request.POST.get('nombre')  # Recuperar el nombre del formulario

        # Verificar si el código de autorización ya existe
        if Codigoautorizacion.objects.filter(codigo_autorizacion=codigo_autorizacion).exists():
            return JsonResponse({'error': 'El código de autorización ya existe'}, status=400)

        # Verificar que el RUC tenga exactamente 10 dígitos
        if len(ruc) != 10 or not ruc.isdigit():
            return JsonResponse({'error': 'El RUC ingresado no es válido'}, status=400)

        # Agregar "001" al final del RUC
        ruc_con_ceros = ruc + "001"

        # Crear un nuevo registro en Codigoautorizacion
        Codigoautorizacion.objects.create(
            id_administrador=id_administrador,
            codigo_autorizacion=codigo_autorizacion,
            fecha_vencimiento=fecha_vencimiento,
            fecha_autorizacion=fecha_autorizacion,
            ruc=ruc_con_ceros,  # Utilizar el RUC modificado
            nombre=nombre  # Agregar el nombre al nuevo registro
        )

        # Retornar una respuesta JSON
        return JsonResponse({'mensaje': 'Codigoautorizacion creado exitosamente'})
    else:
        # Si la solicitud no es POST, retornar un error
        return JsonResponse({'error': 'Se esperaba una solicitud POST'}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class ValidarFactura(View):
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                id_usuario = kwargs.get('id_cuenta')
                mesero = Meseros.objects.get(id_cuenta=id_usuario)
                id_mesero = mesero.id_mesero

                punto_facturacion = get_object_or_404(Puntofacturacion, id_mesero=id_mesero)

                codigo_factura, numero_factura_desde, numero_factura_hasta = Codigosri.obtener_proximo_numero_factura(
                    punto_facturacion.id_puntofacturacion, punto_facturacion.id_administrador.id_sucursal)

                factura_id = kwargs.get('id_factura')
                factura = get_object_or_404(Factura, id_factura=factura_id)

                # Obtener el pedido asociado a la factura
                pedido = factura.id_pedido

                # Verificar si el tipo de pedido es "D" y el estado de pago es "Denegado"
                if pedido.tipo_de_pedido == 'D' and pedido.estado_pago == 'Denegado':
                    return JsonResponse({'error': 'El tipo de pedido es "D", y el estado de pago del pedido asociado es "Denegado". La factura no puede ser validada.'}, status=400)

                # Verificar si el estado de pago del pedido asociado es "Denegado" o "En revisión"
                if pedido.estado_pago in ['Denegado', 'En revisión']:
                    return JsonResponse({'error': f'El estado de pago del pedido asociado es "{pedido.estado_pago}", no se puede validar la factura.'}, status=400)

                # Verificar si el tipo de pedido es "L" y el estado de pago es "En Revisión"
                if pedido.tipo_de_pedido == 'L' and pedido.estado_pago == 'En Revisión':
                    # Cambiar el estado de pago a "Pagado"
                    pedido.estado_pago = 'Pagado'
                    pedido.save()
                    
                # Actualizar los detalles de la factura
                factura.codigo_factura = codigo_factura
                factura.numero_factura_desde = numero_factura_desde
                factura.numero_factura_hasta = numero_factura_hasta

                factura.id_punto_facturacion = punto_facturacion  # Establecer el punto de facturación que validó la factura
                factura.save()

                return JsonResponse({'mensaje': 'Factura validada con éxito'})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=400) 

@csrf_exempt
def crear_punto_facturacion(request, id_cuenta):
    if request.method == 'POST':
        id_administrador = Administrador.objects.get(id_cuenta=id_cuenta)

        # Recuperar los datos del formulario POST
        nombre_punto = request.POST.get('nombre_punto')
        id_mesero_id = request.POST.get('id_mesero')  # Asumiendo que este es el ID del mesero
        sestado = request.POST.get('sestado')
        ruc = request.POST.get('ruc')

        # Asegurarse de que el RUC tenga 10 dígitos y agregar los 3 últimos dígitos como "001"
        if len(ruc) == 10:
            ruc += "001"
        elif len(ruc) != 13:
            return JsonResponse({'error': 'El RUC debe tener 10 dígitos'}, status=400)

        # Obtener el último código de punto de venta registrado
        ultimo_codigo_punto_venta = Puntofacturacion.objects.order_by('-codigo').first()

        if ultimo_codigo_punto_venta:
            ultimo_codigo = int(ultimo_codigo_punto_venta.codigo)
            nuevo_codigo = str(ultimo_codigo + 1).zfill(3)  # Incrementar en 1 y formatear a 3 dígitos
        else:
            nuevo_codigo = '001'  # Si no hay ningún punto de venta registrado, empezar desde '001'

        # Crear un nuevo registro en Puntofacturacion
        nuevo_punto_venta = Puntofacturacion.objects.create(
            id_administrador=id_administrador,
            nombrepunto=nombre_punto,
            codigo=nuevo_codigo,
            id_mesero_id=id_mesero_id,
            sestado=sestado,
            ruc=ruc
            # Otras columnas que puedas tener en tu modelo
        )

        # Retornar una respuesta JSON
        return JsonResponse({'mensaje': 'Punto de facturación creado exitosamente', 'codigo_generado': nuevo_codigo})
    else:
        # Si la solicitud no es POST, retornar un error
        return JsonResponse({'error': 'Se esperaba una solicitud POST'}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class ValidarPuntoFacturacion(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            id_mesero = data.get('id_mesero')

            # Verificar si ya existe un punto de facturación asociado al mesero
            if Puntofacturacion.objects.filter(id_mesero=id_mesero).exists():
                return JsonResponse({'mensaje': 'Ya existe un punto de facturación asociado a este mesero'}, status=400)

            # Si no existe, se puede proceder a crear uno nuevo
            return JsonResponse({'mensaje': 'No existe un punto de facturación asociado a este mesero'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
def validar_permisos(id_usuario):
    try:
        mesero = Meseros.objects.get(id_cuenta=id_usuario)
        # Verificar si el mesero está asociado a algún punto de facturación
        if Puntofacturacion.objects.filter(id_mesero=mesero).exists():
            return True  # Si está asociado a algún punto de facturación, tiene permiso
        else:
            return False  # Si no está asociado a ningún punto de facturación, no tiene permiso
    except Meseros.DoesNotExist:
        return False  # Si no se encuentra el mesero, no tiene permiso

@method_decorator(csrf_exempt, name='dispatch')
class ValidarPermisosFactura(View):
    def get(self, request, *args, **kwargs):
        try:
            id_usuario = kwargs.get('id_cuenta')
            if validar_permisos(id_usuario):
                return JsonResponse({'mensaje': 'Tiene permiso para validar facturas'})
            else:
                return JsonResponse({'error': 'Acceso bloqueado: No tiene permiso para validar facturas'}, status=403)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class VerCodigos(View):
    def get(self, request, *args, **kwargs):
        try:
            # Obtener códigos de autorización
            codigos_autorizacion = Codigoautorizacion.objects.all()
            codigos_autorizacion_data = []

            for codigo_autorizacion in codigos_autorizacion:
                codigo_autorizacion_data = {
                    'id_codigosauto': codigo_autorizacion.id_codigosauto,
                    'id_administrador': codigo_autorizacion.id_administrador_id,  # Obtener solo el ID del administrador
                    'codigo_autorizacion': codigo_autorizacion.codigo_autorizacion,
                    'fecha_vencimiento': str(codigo_autorizacion.fecha_vencimiento),  # Convertir a cadena para JSON
                    'fecha_autorizacion': str(codigo_autorizacion.fecha_autorizacion),  # Convertir a cadena para JSON
                    'ruc': codigo_autorizacion.ruc,
                    'nombre': codigo_autorizacion.nombre,
                }
                codigos_autorizacion_data.append(codigo_autorizacion_data)

            return JsonResponse({'codigos_autorizacion': codigos_autorizacion_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)