from django.views import View
from django.http import JsonResponse
from django.db import transaction
from .models import RecompensasCombos, RecompensasProductos
from Combos.models import Combo
from Producto.models import Producto
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class CrearRecompensaCombo(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            id_combo = request.POST.get('id_combo')
            puntos_recompensa_combo = request.POST.get('puntos_recompensa_combo')
            sestado = request.POST.get('sestado')

            combo = Combo.objects.get(id_combo=id_combo)
            recompensa_combo = RecompensasCombos.objects.create(
                id_combo=combo,
                puntos_recompensa_combo=puntos_recompensa_combo,
                sestado=sestado
            )
            recompensa_combo.save()

            return JsonResponse({'mensaje': 'Recompensa de combo creada con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class CrearRecompensaProducto(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            id_producto = request.POST.get('id_producto')
            puntos_recompensa_producto = request.POST.get('puntos_recompensa_producto')
            sestado = request.POST.get('sestado')

            producto = Producto.objects.get(id_producto=id_producto)
            recompensa_producto = RecompensasProductos.objects.create(
                id_producto=producto,
                puntos_recompensa_producto=puntos_recompensa_producto,
                sestado=sestado
            )
            recompensa_producto.save()

            return JsonResponse({'mensaje': 'Recompensa de producto creada con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ListaRecompensasCombo(View):
    def get(self, request, *args, **kwargs):
        try:
            recompensas_combos = RecompensasCombos.objects.all()
            data = []

            for recompensa_combo in recompensas_combos:
                combo_data = {
                    'id_recompensa_combo': recompensa_combo.id_recompensacombo,
                    'id_combo': recompensa_combo.id_combo.id_combo,
                    'puntos_recompensa_combo': recompensa_combo.puntos_recompensa_combo,
                    'sestado': recompensa_combo.sestado
                }
                data.append(combo_data)

            return JsonResponse({'recompensas_combos': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class ListaRecompensasProducto(View):
    def get(self, request, *args, **kwargs):
        try:
            recompensas_productos = RecompensasProductos.objects.all()
            data = []

            for recompensa_producto in recompensas_productos:
                producto_data = {
                    'id_recompensa_producto': recompensa_producto.id_recompensaproducto,
                    'id_producto': recompensa_producto.id_producto.id_producto,
                    'puntos_recompensa_producto': recompensa_producto.puntos_recompensa_producto,
                    'sestado': recompensa_producto.sestado
                }
                data.append(producto_data)

            return JsonResponse({'recompensas_productos': data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class EditarRecompensaCombo(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            recompensa_combo_id = kwargs.get('recompensa_combo_id') 
            recompensa_combo = RecompensasCombos.objects.get(id_recompensacombo=recompensa_combo_id)
            recompensa_combo.puntos_recompensa_combo = request.POST.get('puntos_recompensa_combo', recompensa_combo.puntos_recompensa_combo)
            recompensa_combo.sestado = request.POST.get('sestado', recompensa_combo.sestado)
            recompensa_combo.save()

            return JsonResponse({'mensaje': 'Recompensa de combo editada con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class EditarRecompensaProducto(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            recompensa_producto_id = kwargs.get('recompensa_producto_id') 
            recompensa_producto = RecompensasProductos.objects.get(id_recompensaproducto=recompensa_producto_id)
            recompensa_producto.puntos_recompensa_producto = request.POST.get('puntos_recompensa_producto', recompensa_producto.puntos_recompensa_producto)
            recompensa_producto.sestado = request.POST.get('sestado', recompensa_producto.sestado)
            recompensa_producto.save()

            return JsonResponse({'mensaje': 'Recompensa de producto editada con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ListarProductosConRecompensas(View):
    def get(self, request, *args, **kwargs):
        try:
            recompensas_productos = RecompensasProductos.objects.all()
            productos_con_recompensas = [recompensa.id_producto.id_producto for recompensa in recompensas_productos]

            return JsonResponse({'productos_con_recompensas': productos_con_recompensas})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500) 

@method_decorator(csrf_exempt, name='dispatch')
class ListarCombosConRecompensas(View):
    def get(self, request, *args, **kwargs):
        try:
            recompensas_combos = RecompensasCombos.objects.all()
            combos_con_recompensas = [recompensa.id_combo.id_combo for recompensa in recompensas_combos]

            return JsonResponse({'combos_con_recompensas': combos_con_recompensas})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        

