from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.db import transaction
from .models import Tipopago, Empresa
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import traceback

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

            # Crear una lista con los datos de cada Tipopago
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
            # Obtener los datos de la solicitud
            id_empleado = request.POST.get('id_empleado')
            fecha_inicio_str = request.POST.get('fecha_inicio')
            fecha_fin_str = request.POST.get('fecha_fin')
            cantidad_pago = request.POST.get('cantidad_pago')

            # Convertir las fechas a objetos datetime
            fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d %H:%M:%S")
            fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d %H:%M:%S")

            # Consultar el Tipopago correspondiente al rol del empleado
            empleado_tipopago = Tipopago.objects.get(rol='X')  # Modifica esto según la lógica de tu aplicación

            # Crear un nuevo periodo
            periodo = Periodo.objects.create(rol='X', desde=fecha_inicio, hasta=fecha_fin)

            # Crear un nuevo pago
            pago = Pagos.objects.create(
                id_empleado=id_empleado,
                cantidad=cantidad_pago,
                tipo_pago=empleado_tipopago.tipo_pago,
                id_periodo=periodo,
                hora_de_pago=datetime.now(),
            )

            return JsonResponse({'mensaje': 'Pago creado con éxito'})

        except Empresa.DoesNotExist:
            return JsonResponse({'error': 'Empresa no encontrada'}, status=404)
        except Tipopago.DoesNotExist:
            return JsonResponse({'error': 'Tipopago no encontrado para el rol del empleado'}, status=404)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=400)