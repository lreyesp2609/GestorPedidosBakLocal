from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Mesero,JefeCocina,Motorizado,Administrador
from Login.models import Cuenta
from django.views import View
from django.db import transaction
from Administrador.models import Administrador
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from Sucursal.models import Sucursales
import json
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_protect

@method_decorator(csrf_exempt, name='dispatch')
class CrearUsuarioView(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            #cuenta = Cuenta.objects.get(nombreusuario=request.user.username)
            #if cuenta.rol != 'S':
                #return JsonResponse({'error': 'No tienes permisos para crear una sucursal'}, status=403)
            data = json.loads(request.body)
            nombre_usuario = data.get('nombreusuario')
            contrasenia = data.get('contrasenia')
            tipo_empleado = data.get('tipo_empleado')
            obs = data.get('observacion')
            correo=data.get('correorecuperacion')

            user = User.objects.create_user(username=nombre_usuario, password=contrasenia)

            cuenta_nueva = Cuenta.objects.create(
                nombreusuario=nombre_usuario,
                contrasenia=make_password(contrasenia),
                estadocuenta='1',
                rol=tipo_empleado,
                observacion=obs,
                correorecuperacion=correo
            )

            # Crear un nuevo empleado según el tipo especificado
            if tipo_empleado == 'X':
                empleado_nuevo = JefeCocina.objects.create(
                    id_sucursal=Sucursales.objects.get(id_sucursal=data.get('id_sucursal')),
                    id_administrador=Administrador.objects.first(),
                    nombre=data.get('nombre'),
                    apellido=data.get('apellido'),
                    telefono=data.get('telefono'),
                    id_cuenta=cuenta_nueva,
                    sestado=1
                )
            elif tipo_empleado == 'M':
                empleado_nuevo = Mesero.objects.create(
                    id_sucursal=Sucursales.objects.get(id_sucursal=data.get('id_sucursal')),
                    id_administrador=Administrador.objects.first(),
                    telefono=data.get('telefono'),
                    apellido=data.get('apellido'),
                    nombre=data.get('nombre'),
                    id_cuenta=cuenta_nueva,
                    sestado=1
                )
            elif tipo_empleado == 'D':
                empleado_nuevo = Motorizado.objects.create(
                    id_sucursal=Sucursales.objects.get(id_sucursal=data.get('id_sucursal')),
                    id_administrador=Administrador.objects.first(),
                    nombre=data.get('nombre'),
                    apellido=data.get('apellido'),
                    telefono=data.get('telefono'),
                    id_cuenta=cuenta_nueva,
                    sestado=1
                )
            else:
                # Si el tipo de empleado no es reconocido, puedes manejarlo según tus necesidades
                raise ValueError('Tipo de empleado no válido')

            return JsonResponse({'mensaje': 'Usuario y empleado creado con éxito'})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)  
def listar_empleados(request, **kwargs):
    try:
        idsucursal = kwargs.get('idsucursal') 
        if idsucursal:
            jefes_cocina = JefeCocina.objects.filter(id_sucursal=idsucursal) if idsucursal else JefeCocina.objects.all()
            motorizados = Motorizado.objects.filter(id_sucursal=idsucursal) if idsucursal else Motorizado.objects.all()
            administradores = Administrador.objects.filter(id_sucursal=idsucursal) if idsucursal else Administrador.objects.all()
            meseros = Mesero.objects.filter(id_sucursal=idsucursal) if idsucursal else Mesero.objects.all()
        else:
            jefes_cocina = JefeCocina.objects.all()
            motorizados = Motorizado.objects.all()
            administradores = Administrador.objects.all()
            meseros = Mesero.objects.all()
        empleados = {
            'JefesCocina': [{'id': j.id_jefecocina, 'tipo': 'X', 'sucursal': j.id_sucursal.id_sucursal if j.id_sucursal else None, 'nombre': j.nombre, 'apellido': j.apellido, 'telefono': j.telefono} for j in jefes_cocina],
            'Motorizados': [{'id': mo.id_motorizado, 'tipo': 'D', 'sucursal': mo.id_sucursal.id_sucursal if mo.id_sucursal else None, 'nombre': mo.nombre, 'apellido': mo.apellido, 'telefono': mo.telefono} for mo in motorizados],
            'Administradores': [{'id': a.id_administrador, 'tipo': 'A', 'sucursal': a.id_sucursal.id_sucursal if a.id_sucursal else None, 'nombre': a.nombre, 'apellido': a.apellido, 'telefono': a.telefono} for a in administradores],
            'Meseros': [{'id': m.id_mesero, 'tipo': 'M', 'sucursal': m.id_sucursal.id_sucursal if m.id_sucursal else None, 'nombre': m.nombre, 'apellido': m.apellido, 'telefono': m.telefono} for m in meseros],
        }

        return JsonResponse({'empleados': empleados})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class EditarEmpleadoView(View):
    template_name = 'editar_empleado.html'

    def post(self, request, tipo_empleado, empleado_id, *args, **kwargs):
        try:
            # Obtener el empleado según el tipo
            if tipo_empleado == 'X':
                empleado = get_object_or_404(JefeCocina, id_jefecocina=empleado_id)
            elif tipo_empleado == 'D':
                empleado = get_object_or_404(Motorizado, id_motorizado=empleado_id)
            elif tipo_empleado == 'M':
                empleado = get_object_or_404(Mesero, id_mesero=empleado_id)
            else:
                # Manejar el tipo de empleado no reconocido según tus necesidades
                return JsonResponse({'error': 'Tipo de empleado no válido'}, status=400)

            # Actualizar los datos del empleado según la entrada del formulario
            data = json.loads(request.body)
            empleado.nombre = data.get('nombre')
            empleado.apellido = data.get('apellido')
            empleado.telefono = data.get('telefono')
            empleado.id_sucursal = Sucursales.objects.get(id_sucursal=data.get('sucursales'))
            empleado.save()

            return JsonResponse({'mensaje': 'Empleado actualizado con éxito'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)