from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from .models import Proveedores
from Administrador.models import Administrador

@method_decorator(csrf_exempt, name='dispatch')
class CrearProveedor(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            nombre_proveedor = request.POST.get('nombreproveedor')
            direccion_proveedor = request.POST.get('direccionproveedor')
            telefono_proveedor = request.POST.get('telefonoproveedor')
            correo_proveedor = request.POST.get('correoproveedor')
            estado_proveedor = request.POST.get('sestado')

            if not nombre_proveedor or estado_proveedor is None:
                raise ValueError("Nombre proveedor y estado son obligatorios")
            
            if Proveedores.objects.filter(telefonoproveedor=telefono_proveedor).exists():
                raise ValueError("Ya existe un proveedor con ese número de teléfono")

            if correo_proveedor:
             if Proveedores.objects.filter(correoproveedor=correo_proveedor).exists():
                raise ValueError("Ya existe un proveedor con ese correo electrónico")


            id_administrador = Administrador.objects.first()

            proveedor = Proveedores(
                nombreproveedor=nombre_proveedor,
                direccionproveedor=direccion_proveedor,
                telefonoproveedor=telefono_proveedor,
                correoproveedor=correo_proveedor,
                id_administrador=id_administrador,
                sestado=estado_proveedor
            )

            proveedor.save()

            return JsonResponse({'mensaje': 'Proveedor creado con éxito'})
        except ValueError as ve:
            return JsonResponse({'error': str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class EditarProveedor(View):
    @transaction.atomic
    def post(self, request, proveedor_id, *args, **kwargs):
        try:
            proveedor = Proveedores.objects.get(id_proveedor=proveedor_id)

            nombre_proveedor = request.POST.get('nombreproveedor', proveedor.nombreproveedor)
            direccion_proveedor = request.POST.get('direccionproveedor', proveedor.direccionproveedor)
            telefono_proveedor = request.POST.get('telefonoproveedor', proveedor.telefonoproveedor)
            correo_proveedor = request.POST.get('correoproveedor', proveedor.correoproveedor)
            estado_proveedor = request.POST.get('sestado', proveedor.sestado)

            proveedor.nombreproveedor = nombre_proveedor
            proveedor.direccionproveedor = direccion_proveedor
            proveedor.telefonoproveedor = telefono_proveedor
            proveedor.correoproveedor = correo_proveedor
            proveedor.sestado = estado_proveedor

            proveedor.save()

            return JsonResponse({'mensaje': 'Proveedor editado con éxito'})
        except Proveedores.DoesNotExist:
            return JsonResponse({'error': 'Proveedor no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
class ListarProveedores(View):
    def get(self, request, *args, **kwargs):
        try:
            proveedores = Proveedores.objects.all()
            proveedores_list = []

            for proveedor in proveedores:
                proveedor_info = {
                    'id_proveedor': proveedor.id_proveedor,
                    'nombreproveedor': proveedor.nombreproveedor,
                    'direccionproveedor': proveedor.direccionproveedor,
                    'telefonoproveedor': proveedor.telefonoproveedor,
                    'correoproveedor': proveedor.correoproveedor,
                    'sestado': proveedor.sestado,
                }
                proveedores_list.append(proveedor_info)

            return JsonResponse({'proveedores': proveedores_list}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)