from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.db import transaction
from .models import Tipopago, Empresa,Periodo,Pagos
from Login.models import Cuenta
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from datetime import datetime
import traceback
from django.utils import timezone
from django.db.models import Min, Max

@method_decorator(csrf_exempt, name='dispatch')
class CrearEditarTipopago(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            # Obtener los datos de la solicitud
            rol = request.POST.get('rol')
            tipo_pago = request.POST.get('tipo_pago')
            cantidad = request.POST.get('cantidad')

            # Verificar si ya existe un Tipopago con el mismo rol
            existing_tipopago = Tipopago.objects.filter(rol=rol).first()

            if existing_tipopago:
                tipopago = existing_tipopago
                mensaje_respuesta = 'Tipopago editado con éxito'
            else:
                tipopago = Tipopago()
                mensaje_respuesta = 'Tipopago creado con éxito'

            tipopago.idempresa = Empresa.objects.all().first()
            tipopago.rol = rol
            tipopago.tipo_pago = tipo_pago
            tipopago.cantidad = cantidad  # Aquí asignamos la cantidad
            tipopago.save()

            return JsonResponse({'mensaje': mensaje_respuesta})

        except Empresa.DoesNotExist:
            return JsonResponse({'error': 'Empresa no encontrada'}, status=404)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class ConsultarTipopago(View):
    def get(self, request, *args, **kwargs):
        try:
            # Consultar todos los Tipopago
            tipopagos = Tipopago.objects.all()

            # Crear una lista con  datos de cada Tipopago
            tipopagos_data = [
                {
                    'id_tipopago': tipopago.id_tipopago,
                    'idempresa': tipopago.idempresa.id_empresa,
                    'rol': tipopago.rol,
                    'tipo_pago': tipopago.tipo_pago,
                    'cantidad': tipopago.cantidad,
                }
                for tipopago in tipopagos
            ]

            return JsonResponse({'tipopagos': tipopagos_data})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class CrearPago(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                id_empleado = request.POST.get('id_empleado')
                fecha_inicio_str = request.POST.get('fecha_inicio')
                fecha_fin_str = request.POST.get('fecha_fin')
                rol = request.POST.get('rol')
                fecha_inicio = datetime.strptime(fecha_inicio_str, "%m/%d/%Y")
                fecha_fin = datetime.strptime(fecha_fin_str, "%m/%d/%Y")
                periodoselec = Periodo.objects.filter(desde=fecha_inicio,hasta=fecha_fin)
                tpago=Tipopago.objects.get(rol=rol)
                empleado=Cuenta.objects.get(id_cuenta=id_empleado)
                if periodoselec.exists():
                    pago=Pagos.objects.filter(idempleado=empleado,idperiodo=periodoselec.first())
                    if pago.exists():
                        return JsonResponse({'error': 'El empleado ya tenía un pago de esa fecha'}, status=400)
                    pago=Pagos.objects.create(
                        idempleado=empleado,
                        cantidad=tpago.cantidad,
                        tipopago=tpago.tipo_pago,
                        idperiodo=periodoselec.first(),
                        horadepago=timezone.now()
                    )
                    return JsonResponse({'mensaje': 'Pago creado con éxito'})
                periodoac=Periodo.objects.create(
                    rol = rol,
                    desde = fecha_inicio,
                    hasta = fecha_fin
                )
                pago=Pagos.objects.create(
                    idempleado=empleado,
                    cantidad=tpago.cantidad,
                    tipopago=tpago.tipo_pago,
                    idperiodo=periodoac,
                    horadepago=timezone.now()
                )

                return JsonResponse({'mensaje': 'Pago creado con éxito'})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class ConsultarPagos(View):
    def get(self, request, *args, **kwargs):
        try:
            # Consultar todos los Pagos
            pagos = Pagos.objects.all()
            
             # Obtener la fecha mínima y máxima de registro
            fecha_minima = pagos.aggregate(min_fecha=Min('horadepago'))['min_fecha']
            fecha_maxima = pagos.aggregate(max_fecha=Max('horadepago'))['max_fecha']

            # Crear una lista con los datos de cada Pago
            pagos_data = [
                {
                    'id_pago': pago.id_pago,
                    'idempleado': pago.idempleado.id_cuenta,
                    'nombre': pago.idempleado.nombreusuario,
                    'cantidad': str(pago.cantidad),  # Convertir el Decimal a cadena para evitar errores de serialización JSON
                    'tipopago': pago.tipopago,
                    'idperiodo': pago.idperiodo.id_periodo,
                    'horadepago': pago.horadepago.strftime('%Y-%m-%d %H:%M:%S'), 
                }
                for pago in pagos
            ]

            return JsonResponse({'pagos': pagos_data, 'fecha_minima': fecha_minima, 'fecha_maxima': fecha_maxima})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)