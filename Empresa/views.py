from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from Empleados.models import *
from django.db import transaction
from PIL import Image
import base64
from io import BytesIO
import json

from .models import Empresa

@method_decorator(csrf_exempt, name='dispatch')
class EmpresaDatosView(View):
    def post(self, request, *args, **kwargs):
        try:

            empresa = Empresa.objects.first()

            if empresa:
                imagen_base64 = None

                if empresa.elogo:
                    try:
                        byteImg = base64.b64decode(empresa.elogo)
                        imagen_base64 = base64.b64encode(byteImg).decode('utf-8')
                    except Exception as img_error:
                        print(f"Error al procesar imagen: {str(img_error)}")
                empresa_info = {
                    'id_empresa': empresa.id_empresa,
                    'enombre': empresa.enombre,
                    'direccion': empresa.direccion,
                    'etelefono': empresa.etelefono,
                    'correoelectronico': empresa.correoelectronico,
                    'fechafundacion': empresa.fechafundacion,
                    'sitioweb': empresa.sitioweb,
                    'eslogan': empresa.eslogan,
                    'empleados':cantidaEmp(0),
                    'edescripcion':empresa.edescripcion,
                    'docmenu':empresa.docmenu,
                    'elogo':imagen_base64,

                }

                # Devuelve la información como respuesta JSON
                return JsonResponse({'mensaje': 'Datos de la empresa', 'empresa_info': empresa_info})
            else:
                return JsonResponse({'mensaje': 'No hay registros en la tabla Empresa'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
def cantidaEmp(ids):
        if ids:
            jefes_cocina = JefeCocina.objects.filter(id_sucursal=ids).count()
            motorizados = Motorizado.objects.filter(id_sucursal=ids).count()
            administradores = Administrador.objects.filter(id_sucursal=ids).count()
            meseros = Mesero.objects.filter(id_sucursal=ids).count()
        else:
            jefes_cocina = JefeCocina.objects.all().count()
            motorizados = Motorizado.objects.all().count()
            administradores = Administrador.objects.all().count()
            meseros = Mesero.objects.all().count()
        return jefes_cocina + motorizados + administradores + meseros

@method_decorator(csrf_exempt, name='dispatch')
class EditarEmpresaDatosView(View):
    def post(self, request, *args, **kwargs):
        empresa= Empresa.objects.first()

        empresa.enombre = request.POST.get('enombre', empresa.enombre)
        empresa.direccion = request.POST.get('direccion', empresa.direccion)
        empresa.etelefono = request.POST.get('etelefono', empresa.etelefono)
        empresa.correoelectronico = request.POST.get('correoelectronico', empresa.correoelectronico)
        empresa.fechafundacion = request.POST.get('fechafundacion', empresa.fechafundacion)
        empresa.sitioweb = request.POST.get('sitioweb', empresa.sitioweb)
        empresa.eslogan = request.POST.get('eslogan', empresa.eslogan)
        empresa.edescripcion = request.POST.get('edescripcion', empresa.edescripcion)
        empresa.docmenu = request.FILES.get('docmenu', empresa.docmenu)
        imagen_p = request.FILES.get('elogo')
        image_64_encode=None
        if imagen_p:
                try:
                    
                    image_read = imagen_p.read()
                    image_64_encode = base64.b64encode(image_read)
                    image_encoded = image_64_encode.decode('utf-8')
                    empresa.elogo = image_64_encode
                except UnidentifiedImageError as img_error:
                    return JsonResponse({'error': f"Error al procesar imagen: {str(img_error)}"}, status=400)
        

        empresa.save()

        return JsonResponse({'mensaje': 'Datos de la empresa actualizados correctamente'})
@method_decorator(csrf_exempt, name='dispatch')
class EditarCombo(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            combo_id = kwargs.get('combo_id')
            combo = Combo.objects.get(id_combo=combo_id)

            # Resto del código para actualizar campos del combo...
            combo.id_catcombo = CategoriasCombos.objects.get(id_catcombo=request.POST.get('id_catcombo', combo.id_catcombo.id_catcombo))
            combo.puntoscb = request.POST.get('puntoscb', combo.puntoscb)
            combo.nombrecb = request.POST.get('nombrecb', combo.nombrecb)
            combo.descripcioncombo = request.POST.get('descripcioncombo', combo.descripcioncombo)
            combo.preciounitario = request.POST.get('preciounitario', combo.preciounitario)
            combo.iva = request.POST.get('iva', combo.iva)
            combo.ice = request.POST.get('ice', combo.ice)
            combo.irbpnr = request.POST.get('irbpnr', combo.irbpnr)

            # Manejo de la imagen
            imagencategoria = request.FILES.get('imagencategoria', None)
            if imagencategoria:
                try:
                    image_read = imagencategoria.read()
                    image_64_encode = base64.b64encode(image_read)
                    image_encoded = image_64_encode.decode('utf-8')
                    combo.imagenc = image_64_encode

                except UnidentifiedImageError as img_error:
                    return JsonResponse({'error': f"Error al procesar imagen: {str(img_error)}"}, status=400)

            # Eliminar los detalles actuales del combo
            combo.detallecombo_set.all().delete()

            # Procesar los nuevos detalles del combo
            detalle_combo_data = json.loads(request.POST.get('detalle_combo', '[]'))
            for detalle_data in detalle_combo_data:
                id_producto = detalle_data.get('id_producto')
                cantidad = detalle_data.get('cantidad')
                producto = Producto.objects.get(id_producto=id_producto)

                # Crea y guarda el detalle del combo
                DetalleCombo.objects.create(
                    id_combo=combo,
                    id_producto=producto,
                    cantidad=cantidad
                )

                # Actualizar valores de IVA, ICE e IRBPNR del combo según el producto
                combo.iva = '1' if producto.iva == '1' else combo.iva
                combo.ice = '1' if producto.ice == '1' else combo.ice
                combo.irbpnr = '1' if producto.irbpnr == '1' else combo.irbpnr

            combo.save()

            return JsonResponse({'mensaje': 'Combo editado con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
