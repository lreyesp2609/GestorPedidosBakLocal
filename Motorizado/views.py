from datetime import timezone
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from Mesero.models import Pedidos
from Motorizado.models import CajaDiaria, Motorizados, PedidosMotorizado
from Motorizado.serializer import PedidoSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@api_view(['GET'])
def pedidos_domicilio(request):
    # Filtramos los pedidos por tipo "D" (domicilio)
    pedidos = Pedidos.objects.filter(tipo_de_pedido='D')
    
    # Serializamos los pedidos
    serializer = PedidoSerializer(pedidos, many=True)
    
    # Devolvemos la respuesta en formato JSON
    return Response(serializer.data)

@csrf_exempt
def aceptar_pedido(request):
    if request.method == 'POST':
        try:
            # Leer los datos del cuerpo de la solicitud
            data = json.loads(request.body)
            id_motorizado = data.get('id_motorizado')
            id_pedido = data.get('id_pedido')
            cantidad = data.get('cantidad', 1)  # Por defecto, acepta 1 pedido

            # Verificar que el motorizado y el pedido existan
            motorizado = Motorizados.objects.get(id_motorizado=id_motorizado)
            pedido = Pedidos.objects.get(id_pedido=id_pedido)

            # Actualizar el estado del pedido a 'C' (En Camino)
            pedido.estado_del_pedido = 'C'
            pedido.save()

            # Registrar la aceptación del pedido por el motorizado
            PedidosMotorizado.objects.create(
                id_motorizado=motorizado,
                id_pedido=pedido,
                cantidad=cantidad
            )

            return JsonResponse({'status': 'success', 'message': 'Pedido aceptado correctamente.'})
        except Motorizados.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Motorizado no encontrado.'}, status=404)
        except Pedidos.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Pedido no encontrado.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)
    
@csrf_exempt
def entregar_pedido(request):
    if request.method == 'POST':
        try:
            # Leer los datos del cuerpo de la solicitud
            data = json.loads(request.body)
            id_pedido = data.get('id_pedido')
            id_motorizado = data.get('id_motorizado')

            # Verificar que el pedido y el motorizado existan
            pedido = Pedidos.objects.get(id_pedido=id_pedido)
            motorizado = Motorizados.objects.get(id_motorizado=id_motorizado)

            # Cambiar el estado del pedido a 'E' (Entregado)
            pedido.estado_del_pedido = 'E'
            pedido.save()

            # Obtener o crear la caja diaria del motorizado
            caja_diaria, created = CajaDiaria.objects.get_or_create(
                id_motorizado=motorizado,
                fecha=timezone.now().date(),  # Usar la fecha actual
                defaults={'monto_acumulado': 0}
            )

            # Acumular el monto del pedido en la caja diaria
            caja_diaria.monto_acumulado += pedido.precio
            caja_diaria.save()

            return JsonResponse({'status': 'success', 'message': 'Pedido entregado correctamente.'})
        except Pedidos.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Pedido no encontrado.'}, status=404)
        except Motorizados.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Motorizado no encontrado.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({'status': 'error', 'message': 'Método no permitido.'}, status=405)
    
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone

@api_view(['GET'])
def caja_diaria(request, id_motorizado):
    try:
        # Obtener la caja diaria del motorizado para la fecha actual
        caja_diaria = CajaDiaria.objects.get(
            id_motorizado=id_motorizado,
            fecha=timezone.now().date()
        )
        return Response({'monto_acumulado': caja_diaria.monto_acumulado})
    except CajaDiaria.DoesNotExist:
        return Response({'monto_acumulado': 0})