from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import AvisosPrincipales
from Login.models import Cuenta
from Empresa.models import Empresa
import io
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from PIL import Image, UnidentifiedImageError
from django.core.files.base import ContentFile
import base64
import json
from io import BytesIO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@method_decorator(csrf_exempt, name='dispatch')
class AvisosPrincipalesListView(View):
    def get(self, request, *args, **kwargs):
        try:
            avisos_principales = AvisosPrincipales.objects.all()
            avisos_list = []
            for aviso in avisos_principales:
                if aviso.imagen:
                    try:
                        byteImg = base64.b64decode(aviso.imagen)
                        imagen_base64 = base64.b64encode(byteImg).decode('utf-8')
                        aviso_info = {
                            'id_aviso': aviso.id_aviso,
                            'id_empresa': aviso.id_empresa.id_empresa if aviso.id_empresa else None,
                            'titulo': aviso.titulo,
                            'descripcion': aviso.descripcion,
                            'imagen': imagen_base64,

                        }
                        avisos_list.append(aviso_info)
                    except Exception as img_error:
                        print(f"Error al procesar imagen: {str(img_error)}")
                else:
                    aviso_info = {
                        'id_aviso': aviso.id_aviso,
                        'id_empresa': aviso.id_empresa.id_empresa if aviso.id_empresa else None,
                        'titulo': aviso.titulo,
                        'descripcion': aviso.descripcion,
                        'imagen': None,
                    }
                    avisos_list.append(aviso_info)

            return JsonResponse({'avisos_principales': avisos_list}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class CrearAviso(View):
    #@method_decorator(login_required)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            #cuenta = Cuenta.objects.get(nombreusuario=request.user.username)
            #if cuenta.rol != 'S':
                #return JsonResponse({'error': 'No tienes permisos para crear un aviso'}, status=403)

            titulo = request.POST.get('titulo')
            descripcion = request.POST.get('descripcion')
            if AvisosPrincipales.objects.filter(titulo=titulo).exists():
                return JsonResponse({'error': 'Ya existe un aviso con el mismo título'}, status=400)
            imagen_archivo = request.FILES.get('imagen')
            image_encoded=None
            if imagen_archivo:
                try:
                    image_read = imagen_archivo.read()
                    image_64_encode = base64.b64encode(image_read)
                    image_encoded = image_64_encode.decode('utf-8')
                except UnidentifiedImageError as img_error:
                    return JsonResponse({'error': f"Error al procesar imagen: {str(img_error)}"}, status=400)
            aviso=AvisosPrincipales.objects.create(
                titulo=titulo,
                descripcion=descripcion,
                imagen=image_64_encode,
                id_empresa=Empresa.objects.first(),
                sestado=1
            )
            return JsonResponse({'mensaje': 'Se creo el aviso'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class EditarAviso(View):
    #@method_decorator(login_required)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            aviso_id = kwargs.get('id_aviso')
            aviso = AvisosPrincipales.objects.get(id_aviso=aviso_id)
            aviso.titulo=request.POST.get('titulo')
            aviso.descripcion=request.POST.get('descripcion')
            nueva_imagen = request.FILES.get('nueva_imagen')
            if nueva_imagen:
                try:
                    image_read = nueva_imagen.read()
                    image_64_encode = base64.b64encode(image_read)
                    # No decodificar a utf-8
                    aviso.imagen=image_64_encode
                except UnidentifiedImageError as img_error:
                    return JsonResponse({'error': f"Error al procesar imagen: {str(img_error)}"}, status=400)
            aviso.save()
            return JsonResponse({'mensaje': 'Aviso editado con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class EditarAvisoDos(View):
    #@method_decorator(login_required)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            aviso_id = kwargs.get('id_aviso')
            aviso = AvisosPrincipales.objects.get(id_aviso=aviso_id)
            
            # Si se proporciona un título en la solicitud, actualizarlo
            titulo = request.POST.get('titulo')
            if titulo:
                aviso.titulo = titulo
            
            # Actualizar la descripción si se proporciona
            descripcion = request.POST.get('descripcion')
            if descripcion:
                aviso.descripcion = descripcion
                
            # Actualizar la imagen si se proporciona
            nueva_imagen = request.FILES.get('nueva_imagen')
            if nueva_imagen:
                try:
                    image_read = nueva_imagen.read()
                    image_64_encode = base64.b64encode(image_read)
                    # No decodificar a utf-8
                    aviso.imagen = image_64_encode
                except UnidentifiedImageError as img_error:
                    return JsonResponse({'error': f"Error al procesar imagen: {str(img_error)}"}, status=400)
            
            aviso.save()
            return JsonResponse({'mensaje': 'Aviso editado con éxito'})
        except AvisosPrincipales.DoesNotExist:
            return JsonResponse({'error': 'El aviso especificado no existe'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)