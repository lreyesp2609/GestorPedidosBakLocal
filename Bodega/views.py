from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.db import transaction
from Bodega.models import Bodegas
from Sucursal.models import Sucursales
from Login.models import Cuenta
import json
# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class CrearBodegaView(View):
    #@method_decorator(login_required)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            #cuenta = Cuenta.objects.get(nombreusuario=request.user.username)
            #if cuenta.rol != 'A':
                #return JsonResponse({'error': 'No tienes permisos para crear una bodega'}, status=403)

            data = json.loads(request.body)
            nombrebog = data.get('nombrebog')
            descripcion= data.get('descripcion')
            idsucursal=data.get('id_sucursal')
            bodega_nueva  = Bodegas.objects.create(
                nombrebog=nombrebog,
                descripcion=descripcion,
                id_sucursal =Sucursales.objects.filter(id_sucursal=idsucursal).first(),
                sestado=1
            )

            return JsonResponse({'mensaje': 'Bodega creada con éxito'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

class ListarBodegasView(View):
    def get(self, request, *args, **kwargs):
        try:
            bodegas = Bodegas.objects.all()
            bodegas_list = []
            
            for bodega in bodegas:
                bodegas_list.append({
                    'id_bodega': bodega.id_bodega,
                    'nombrebog': bodega.nombrebog,
                    'descripcion': bodega.descripcion,
                    'id_sucursal': bodega.id_sucursal.id_sucursal,
                })

            return JsonResponse({'bodegas': bodegas_list})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class EditarBodegaView(View):
    def post(self, request, *args, **kwargs):
        try:
            bodega_id = kwargs.get('bodega_id') or kwargs.get('id')
            data = request.POST

            nombrebog = data.get('nombrebog')
            descripcion = data.get('descripcion')
            id_sucursal = data.get('id_sucursal')

            bodega = Bodegas.objects.get(id_bodega=bodega_id)

            bodega.nombrebog = nombrebog
            bodega.descripcion = descripcion

            sucursal = Sucursales.objects.get(id_sucursal=id_sucursal)
            bodega.id_sucursal = sucursal

            bodega.save()

            return JsonResponse({'mensaje': 'Bodega editada con éxito'})

        except Bodegas.DoesNotExist:
            return JsonResponse({'error': 'La bodega no existe'}, status=404)
        except Sucursales.DoesNotExist:
            return JsonResponse({'error': 'La sucursal no existe'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)