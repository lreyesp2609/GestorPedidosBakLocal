# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.utils.decorators import method_decorator
import re

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
                rango_desde=numero_factura_desde,
                rango_hasta=numero_factura_hasta,
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

        # Verificar si el código de autorización ya existe
        if Codigoautorizacion.objects.filter(codigo_autorizacion=codigo_autorizacion).exists():
            return JsonResponse({'error': 'El código de autorización ya existe'}, status=400)

        # Crear un nuevo registro en Codigoautorizacion
        Codigoautorizacion.objects.create(
            id_administrador=id_administrador,
            codigo_autorizacion=codigo_autorizacion,
            fecha_vencimiento=fecha_vencimiento,
            fecha_autorizacion=fecha_autorizacion
        )

        # Retornar una respuesta JSON
        return JsonResponse({'mensaje': 'Codigoautorizacion creado exitosamente'})
    else:
        # Si la solicitud no es POST, retornar un error
        return JsonResponse({'error': 'Se esperaba una solicitud POST'}, status=400)