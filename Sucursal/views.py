import json 
from django.forms.models import model_to_dict
from shapely.geometry import Point, Polygon
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Sucursales
import base64
from datetime import datetime, timezone
from horariossemanales.models import Horariossemanales
from GeoSector.models import Geosectores
from Empresa.models import Empresa
from Ubicaciones.models import Ubicaciones
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from Login.models import Cuenta
from io import BytesIO
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from Empleados.models import *
from GeoSector.models import *
from horariossemanales.models import *
import traceback

from PIL import Image

class SucursalesListView(View):
    def get(self, request, *args, **kwargs):
        try:
            #comentario
            sucursales = Sucursales.objects.all().order_by('id_sucursal')
            paginator = Paginator(sucursales, 200) 
            page = request.POST.get('pageSize')

            try:
                sucursales_list = paginator.page(page)
            except PageNotAnInteger:
                sucursales_list = paginator.page(1)
            except EmptyPage:
                sucursales_list = paginator.page(paginator.num_pages)

            serialized_sucursales = []
            for sucursal in sucursales_list:
                # Código para redimensionar la imagen
                if sucursal.imagensucursal:
                    img = Image.open(BytesIO(base64.b64decode(sucursal.imagensucursal)))
                    img = img.resize((500, 500))
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    imagen_base64_resized = base64.b64encode(buffered.getvalue()).decode('utf-8')
                else:
                    imagen_base64_resized = None
                
                # Información sobre ubicación
                ubicacion_info = {
                    'id_ubicacion': sucursal.id_ubicacion.id_ubicacion if sucursal.id_ubicacion else None,
                    'latitud': sucursal.id_ubicacion.latitud if sucursal.id_ubicacion else None,
                    'longitud': sucursal.id_ubicacion.longitud if sucursal.id_ubicacion else None,
                    'udescripcion': sucursal.id_ubicacion.udescripcion if sucursal.id_ubicacion else None,
                }

                # Información sobre horario
                horario_info = None
                if sucursal.id_horarios_id:
                    horario = Horariossemanales.objects.get(id_horarios=sucursal.id_horarios.id_horarios)
                    detalles_horario = DetalleHorariosSemanales.objects.filter(id_horarios=horario)
                    horario_info = {
                        'nombreh': horario.nombreh,
                        'detalles': [
                            {
                                'dia': detalle.dia,
                                'horainicio': detalle.horainicio.strftime('%H:%M:%S'),
                                'horafin': detalle.horafin.strftime('%H:%M:%S'),
                            }
                            for detalle in detalles_horario
                        ],
                    }

                sucursal_info = {
                    'id_sucursal': sucursal.id_sucursal,
                    'srazon_social': sucursal.srazon_social,
                    'sruc': sucursal.sruc,
                    'sestado': sucursal.sestado,
                    'scapacidad': sucursal.scapacidad,
                    'scorreo': sucursal.scorreo,
                    'stelefono': sucursal.stelefono,
                    'sdireccion': sucursal.sdireccion,
                    'snombre': sucursal.snombre,
                    'fsapertura': sucursal.fsapertura.strftime('%Y-%m-%d') if sucursal.fsapertura else None,
                    'id_horarios': sucursal.id_horarios.id_horarios if hasattr(sucursal, 'id_horarios') else None,
                    'id_geosector': getattr(sucursal.id_geosector, 'id_geosector', None),
                    'firmaelectronica': sucursal.firmaelectronica,
                    'id_empresa': sucursal.id_empresa_id,
                    'id_ubicacion': ubicacion_info,
                    'cantidadempleados':cantidaEmp(sucursal.id_sucursal),
                    'imagensucursal': imagen_base64_resized,
                    'horario': horario_info,
                }
                serialized_sucursales.append(sucursal_info)
            return JsonResponse({'sucursales': serialized_sucursales}, safe=False)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)
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
class Crearsucursal(View):
    #@method_decorator(login_required)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            #cuenta = Cuenta.objects.get(nombreusuario=request.user.username)
            #if cuenta.rol != 'S':
            #    return JsonResponse({'error': 'No tienes permisos para crear una sucursal'}, status=403)
            razon_social = request.POST.get('razonsocial')
            ruc = request.POST.get('sruc')
            capacidad=request.POST.get('capacidad')
            correo= request.POST.get('scorreo')
            telefono= request.POST.get('ctelefono')
            direccion= request.POST.get('sdireccion')
            nombre= request.POST.get('snombre')
            id_horarios=  request.POST.get('horario')
            idgeosector= request.POST.get('geosectorid')
            firmaelectronica = request.POST.get('firma')
            latitudx = request.POST.get('latitud')
            longitudx = request.POST.get('longitud')
            imagen= request.FILES.get('imagen')
            image_64_encode=None
            if imagen:
                try:
                    image_read = imagen.read()
                    image_64_encode = base64.b64encode(image_read)
                    image_encoded = image_64_encode.decode('utf-8')
                except UnidentifiedImageError as img_error:
                    return JsonResponse({'error': f"Error al procesar imagen: {str(img_error)}"}, status=400)
            if latitudx is not None and longitudx is not None:
                try:
                    sucursal_nueva = Sucursales.objects.create(
                        srazon_social=razon_social,
                        sruc=ruc,
                        sestado='1',
                        scapacidad=capacidad,
                        scorreo=correo,
                        stelefono=telefono,
                        sdireccion=direccion,
                        snombre=nombre,
                        id_horarios=Horariossemanales.objects.create(**id_horarios) if id_horarios is not None else None,
                        id_geosector=Geosectores.objects.create(**idgeosector) if idgeosector is not None else None,
                        firmaelectronica=firmaelectronica,
                        id_empresa=Empresa.objects.first(),
                        id_ubicacion=Ubicaciones.objects.create(
                            latitud=latitudx,
                            longitud=longitudx,
                        ),
                        imagensucursal=image_64_encode,
                    )
                    return JsonResponse({'mensaje': 'Sucursal creada con éxito'})
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=400)
            sucursal_nueva  = Sucursales.objects.create(
                srazon_social=razon_social,
                sruc=ruc,
                sestado ='1',
                scapacidad = capacidad,
                scorreo =correo,
                stelefono=telefono,
                sdireccion=direccion,
                snombre=nombre,
                id_horarios=Horariossemanales.objects.create(**id_horarios) if id_horarios is not None else None,
                id_geosector=Geosectores.objects.create(**idgeosector) if idgeosector is not None else None,
                firmaelectronica=firmaelectronica,
                id_empresa=Empresa.objects.first(),
                imagensucursal=image_64_encode,
            )
            return JsonResponse({'mensaje': 'Sucursal creada con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class Editarubicacion(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            id_sucursal = request.POST.get('id_sucursal')
            if id_sucursal is None:
                return JsonResponse({'error': 'ID de sucursal no proporcionado'}, status=400)
            sucursaledit = Sucursales.objects.get(id_sucursal=id_sucursal)
            latitudx = request.POST.get('latitud')
            longitudx = request.POST.get('longitud')
            sucursaledit.id_ubicacion = Ubicaciones.objects.create(latitud=latitudx, longitud=longitudx,sestado=1) if latitudx is not None and longitudx is not None else None
            sucursaledit.save()
            return JsonResponse({'mensaje': 'Sucursal editada con éxito'})
        except Sucursales.DoesNotExist:
            return JsonResponse({'error': 'La sucursal no existe'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class actdesSucursal(View):
    #@method_decorator(login_required)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            #cuenta = Cuenta.objects.get(nombreusuario=request.user.username)
            #if cuenta.rol != 'S':
            #    return JsonResponse({'error': 'No tienes permisos para crear una sucursal'}, status=403)
            id_sucursal = request.POST.get('id_sucursal')
            sestado = request.POST.get('sestado')
            sucursal = Sucursales.objects.get(id_sucursal=id_sucursal)
            if sestado:
                sucursal.sestado=sestado
                sucursal.save()
                return JsonResponse({'mensaje': 'Estado cambiado con exito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class sucursalExist(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            srazon_social = data.get('srazon_social')
            sruc = data.get('sruc')
            snombre = data.get('snombre')
            if srazon_social is not None:
                if Sucursales.objects.filter(srazon_social=srazon_social).first():
                    return JsonResponse({'mensaje': '1'})
            if sruc is not None:
                if Sucursales.objects.filter(sruc=sruc).first():
                    return JsonResponse({'mensaje': '1'})
            if snombre is not None:
                if Sucursales.objects.filter(snombre=snombre).first():
                    return JsonResponse({'mensaje': '1'})
            return JsonResponse({'mensaje': '0'})
        
            
        except Exception as e:
            return JsonResponse({'error xd': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class cargarSucursal(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            id_sucursal = kwargs.get('id_sucursal') 
            sucursal = Sucursales.objects.get(id_sucursal=id_sucursal)
            
            if sucursal.imagensucursal:
                img = Image.open(BytesIO(base64.b64decode(sucursal.imagensucursal)))
                img = img.resize((500, 500))
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                imagen_base64_resized = base64.b64encode(buffered.getvalue()).decode('utf-8')
            else:
                imagen_base64_resized = None
            
            # Obtener información de ubicación del geosector
            geosector_info = None
            if sucursal.id_geosector:
                detalle_geosector = DetalleGeosector.objects.filter(id_geosector=sucursal.id_geosector)
                ubicaciones_geosector = [{
                    'id_ubicacion': detalle.id_ubicacion.id_ubicacion,
                    'latitud': detalle.id_ubicacion.latitud,
                    'longitud': detalle.id_ubicacion.longitud,
                    'udescripcion': detalle.id_ubicacion.udescripcion,
                } for detalle in detalle_geosector]

                geosector_info = {
                    'id_geosector': sucursal.id_geosector.id_geosector,
                    'secnombre': sucursal.id_geosector.secnombre,
                    'secdescripcion': sucursal.id_geosector.secdescripcion,
                    'fechacreaciong': sucursal.id_geosector.fechacreaciong.strftime('%Y-%m-%d %H:%M:%S'),
                    'secestado': sucursal.id_geosector.secestado,
                    'sectipo': sucursal.id_geosector.sectipo,
                    'sestado': sucursal.id_geosector.sestado,
                    'tarifa': sucursal.id_geosector.tarifa,
                    'ubicaciones_geosector': ubicaciones_geosector,
                }

            ubicacion_info = {
                'id_ubicacion': sucursal.id_ubicacion.id_ubicacion if sucursal.id_ubicacion else None,
                'latitud': sucursal.id_ubicacion.latitud if sucursal.id_ubicacion else None,
                'longitud': sucursal.id_ubicacion.longitud if sucursal.id_ubicacion else None,
                'udescripcion': sucursal.id_ubicacion.udescripcion if sucursal.id_ubicacion else None,
            }
            
            cantidad_empleados = cantidaEmp(sucursal.id_sucursal)
            serialized_sucursales = []
            sucursal_info  = {
                'id_sucursal': sucursal.id_sucursal,
                'srazon_social': sucursal.srazon_social,
                'sruc': sucursal.sruc,
                'sestado': sucursal.sestado,
                'scapacidad': sucursal.scapacidad,
                'scorreo': sucursal.scorreo,
                'stelefono': sucursal.stelefono,
                'sdireccion': sucursal.sdireccion,
                'snombre': sucursal.snombre,
                'fsapertura': sucursal.fsapertura.strftime('%Y-%m-%d') if sucursal.fsapertura else None,
                'id_horarios': sucursal.id_horarios.id_horarios if hasattr(sucursal, 'id_horarios') else None,
                'id_geosector': geosector_info,
                'firmaelectronica': sucursal.firmaelectronica,
                'id_empresa': sucursal.id_empresa_id,
                'id_ubicacion': ubicacion_info,
                'cantidadempleados': cantidad_empleados,
                'imagensucursal': imagen_base64_resized,
            }

            serialized_sucursales.append(sucursal_info)
            return JsonResponse({'mensaje': serialized_sucursales})    
        except Exception as e:
            return JsonResponse({'error xd': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class EditarSucursal(View):
    #@method_decorator(login_required)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            #cuenta = Cuenta.objects.get(nombreusuario=request.user.username)
            #if cuenta.rol != 'S':
            #    return JsonResponse({'error': 'No tienes permisos para crear una sucursal'}, status=403)
            id_sucursal = kwargs.get('id_sucursal') 
            sucursal = Sucursales.objects.get(id_sucursal=id_sucursal)
            razon_social = request.POST.get('razonsocial')
            ruc = request.POST.get('sruc')
            capacidad=request.POST.get('capacidad')
            correo= request.POST.get('scorreo')
            telefono= request.POST.get('ctelefono')
            direccion= request.POST.get('sdireccion')
            nombre= request.POST.get('snombre')
            sucursal.srazon_social=razon_social
            sucursal.sruc=ruc
            sucursal.scapacidad = capacidad
            sucursal.scorreo =correo
            sucursal.stelefono=telefono
            sucursal.sdireccion=direccion
            sucursal.snombre=nombre
            imagensucursal = request.FILES.get('imagensucursal')
            if imagensucursal:
                try:
                    image_read = imagensucursal.read()
                    image_64_encode = base64.b64encode(image_read)
                    image_encoded = image_64_encode.decode('utf-8')
                    sucursal.imagensucursal=image_64_encode
                except UnidentifiedImageError as img_error:
                    return JsonResponse({'error': f"Error al procesar imagen: {str(img_error)}"}, status=400)
            sucursal.save()
            return JsonResponse({'mensaje': 'Sucursal editada con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class crearGeosector(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            # Obtener datos del formulario
            secnombre = request.POST.get('secnombre')
            secdescripcion = request.POST.get('secdescripcion')
            id_sucursal = request.POST.get('id_sucursal')
            datos_geosector_str = request.POST.get('datosGeosector','[]')

            # Parsear datos_geosector como JSON
            datos_geosector = json.loads(datos_geosector_str)
            sucursal = Sucursales.objects.get(id_sucursal=id_sucursal)
            # Crear geosector con fecha actual
            geosector = Geosectores.objects.create(
                secnombre=secnombre,
                secdescripcion=secdescripcion,
                fechacreaciong=datetime.now(timezone.utc),
                secestado=1,
                sectipo='C',
                sestado=1,
            )
            sucursal.id_geosector = geosector
            sucursal.save()
            # Asociar el geosector a la sucursal
            

            # Crear ubicaciones y detalle_geosector
            for ubicacion_data in datos_geosector:
                ubicacion = Ubicaciones.objects.create(
                    latitud=ubicacion_data['latitude'],
                    longitud=ubicacion_data['longitude'],
                    sestado=1,
                )

                DetalleGeosector.objects.create(
                    id_geosector=geosector,
                    id_ubicacion=ubicacion,
                )

            return JsonResponse({'mensaje': 'Geosector y sucursal creados con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
class ListarSucursalReporte(View):
    def get(self, request, *args, **kwargs):
        try:
            sucursales = Sucursales.objects.all().order_by('id_sucursal')
            paginator = Paginator(sucursales, 200) 
            page = request.POST.get('pageSize')

            try:
                sucursales_list = paginator.page(page)
            except PageNotAnInteger:
                sucursales_list = paginator.page(1)
            except EmptyPage:
                sucursales_list = paginator.page(paginator.num_pages)

            serialized_sucursales = []
            for sucursal in sucursales_list:
                ubicacion_info = {
                    'direccion': sucursal.sdireccion,
                }

                horario_info = None
                if sucursal.id_horarios_id:
                    horario = Horariossemanales.objects.get(id_horarios=sucursal.id_horarios.id_horarios)
                    detalles_horario = DetalleHorariosSemanales.objects.filter(id_horarios=horario)
                    horario_info = {
                        'nombre': horario.nombreh,
                    }

                sucursal_info = {
                    'nombre': sucursal.snombre,
                    'apertura': sucursal.fsapertura.strftime('%Y-%m-%d') if sucursal.fsapertura else None,
                    'estado': sucursal.sestado,
                    'direccion': ubicacion_info['direccion'],
                    'numcelular': sucursal.stelefono,
                    'total_empleados': self.cantidaEmp(sucursal.id_sucursal),
                }
                serialized_sucursales.append(sucursal_info)
            return JsonResponse({'sucursales': serialized_sucursales}, safe=False)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=500)

    def cantidaEmp(self, ids):
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
class BuscarSucursalPorUbicacion(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            latitud = float(request.POST.get('latitud'))
            longitud = float(request.POST.get('longitud')), 
            # Obtener todas las sucursales de la base de datos
            sucursales = Sucursales.objects.all()
            for sucursal in sucursales:
                geosector_id = sucursal.id_geosector.id_geosector
                geosector = Geosectores.objects.get(id_geosector=geosector_id)
                ubicaciones_geosector = DetalleGeosector.objects.filter(id_geosector=geosector)
                # Crear un polígono con las ubicaciones del geosector
                polygon_coordinates = [(ubicacion.id_ubicacion.latitud, ubicacion.id_ubicacion.longitud) for ubicacion in ubicaciones_geosector]
                polygon = Polygon(polygon_coordinates)
                point = Point(latitud, longitud)
                if point.within(polygon):
                    sucursal_dict = model_to_dict(sucursal)
                    print("Si se devuelve")
                    return JsonResponse({'sucursal': sucursal_dict})
            return JsonResponse({'sucursal': "no hay"})
        except Sucursales.DoesNotExist:
            traceback.print_exc()
            return JsonResponse({'error': 'La sucursal no existe'}, status=404)
        except Exception as e:
            traceback.print_exc() 
            return JsonResponse({'error': str(e)}, status=400)