from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import ReversionMovimientoInventario, MovimientoInventario


@method_decorator(csrf_exempt, name='dispatch')
class GuardarReversionMovimiento(View):
    def post(self, request, movimiento_id):
        try:
            # Obtener el movimiento de inventario existente
            movimiento = get_object_or_404(MovimientoInventario, id_movimientoinventario=movimiento_id)

            # Crear la reversión de movimiento
            ReversionMovimientoInventario.objects.create(
                id_movimientoinventario=movimiento,
                id_cuenta=movimiento.id_cuenta,  # Utilizamos la misma cuenta del movimiento original
                motivo=request.POST.get('motivo', '')  # Se espera que 'motivo' sea enviado en el cuerpo de la solicitud POST
            )

            # Puedes devolver una respuesta JSON indicando que la reversión se guardó correctamente
            return JsonResponse({'mensaje': 'Reversión de movimiento guardada correctamente.'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)