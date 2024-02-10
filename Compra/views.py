from django.http import QueryDict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import *
from django.db import transaction
from django.http import JsonResponse
import json

@method_decorator(csrf_exempt, name='dispatch')
class CrearCompra(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            id_proveedor = request.POST.get('id_proveedor')
            fecha_compra = request.POST.get('fecha_compra')
            id_procesamiento = request.POST.get('id_procesamiento')

            id_administrador = Administrador.objects.first()

            compra = Compras.objects.create(
                id_proveedor_id=id_proveedor,
                id_administrador=id_administrador,
                fechacompra=fecha_compra,
                id_procesamiento_id=id_procesamiento
            )
            compra.save()

            detalle_compra_data = json.loads(request.POST.get('detalle_compra', '[]'))

            for detalle_data in detalle_compra_data:
                id_producto = detalle_data.get('id_producto')
                cantidad = detalle_data.get('cantidad')
                precio = detalle_data.get('precio')
                id_um = detalle_data.get('id_um')
                producto = Producto.objects.get(id_producto=id_producto)

                DetalleCompra.objects.create(
                    id_compra=compra,
                    id_producto=producto,
                    cantidad=cantidad,
                    precio=precio,
                    id_um_id=id_um
                )

            return JsonResponse({'mensaje': 'Compra creada con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)