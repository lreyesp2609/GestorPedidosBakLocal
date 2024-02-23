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

def listar_empleados_tipo(request, idsucursal=None, tipo_empleado=None):
    try:
        empleados_data = []

        # Si se proporciona un tipo de empleado pero no una sucursal
        if tipo_empleado and not idsucursal:
            return JsonResponse({'error': 'Debe especificar una sucursal'}, status=400)
        
        # Si no se proporciona un tipo de empleado ni una sucursal
        if not tipo_empleado and not idsucursal:
            return JsonResponse({'error': 'Debe especificar al menos una sucursal o un tipo de empleado'}, status=400)

        # Si se proporciona tanto una sucursal como un tipo de empleado
        if idsucursal and tipo_empleado:
            if tipo_empleado == 'jefe_cocina':
                empleados = JefeCocina.objects.filter(id_sucursal=idsucursal)
            elif tipo_empleado == 'motorizado':
                empleados = Motorizado.objects.filter(id_sucursal=idsucursal)
            elif tipo_empleado == 'mesero':
                empleados = Mesero.objects.filter(id_sucursal=idsucursal)
            else:
                return JsonResponse({'error': 'Tipo de empleado no válido'}, status=400)

            empleados_data = [{'nombre': empleado.nombre, 'apellido': empleado.apellido, 'telefono': empleado.telefono,  'fecha': empleado.fecha_registro} for empleado in empleados]

            if not empleados_data:
                return JsonResponse({'mensaje': 'No hay empleados de tipo {} en la sucursal {}'.format(tipo_empleado, idsucursal)})

        # Si se proporciona solo una sucursal
        if idsucursal and not tipo_empleado:
            jefes_cocina = JefeCocina.objects.filter(id_sucursal=idsucursal)
            motorizados = Motorizado.objects.filter(id_sucursal=idsucursal)
            meseros = Mesero.objects.filter(id_sucursal=idsucursal)
            
            empleados = list(jefes_cocina) + list(motorizados) + list(meseros)        
            empleados_data = [{'nombre': empleado.nombre, 'apellido': empleado.apellido, 'telefono': empleado.telefono, 'fecha': empleado.fecha_registro} for empleado in empleados]

            if not empleados_data:
                return JsonResponse({'mensaje': 'No hay empleados en la sucursal {}'.format(idsucursal)})

        return JsonResponse({'empleados': empleados_data})
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def listar_todos_los_empleados(request):
    try:
        # Obtener todos los empleados de los diferentes modelos
        meseros = Mesero.objects.prefetch_related('id_sucursal').all()
        jefes_cocina = JefeCocina.objects.prefetch_related('id_sucursal').all()
        motorizados = Motorizado.objects.prefetch_related('id_sucursal').all()

        # Crear una lista para almacenar los datos de todos los empleados
        empleados_data = []

        # Agregar los datos de los meseros
        for mesero in meseros:
            empleados_data.append({
                'sucursal': mesero.id_sucursal.snombre,
                'ciudad': mesero.id_sucursal.sdireccion,
                'nombre': mesero.nombre,
                'apellido': mesero.apellido,
                'telefono': mesero.telefono,
                'fecha': mesero.fecha_registro
            })

        # Agregar los datos de los jefes de cocina
        for jefe_cocina in jefes_cocina:
            empleados_data.append({
                'sucursal': jefe_cocina.id_sucursal.snombre,
                'ciudad': jefe_cocina.id_sucursal.sdireccion,
                'nombre': jefe_cocina.nombre,
                'apellido': jefe_cocina.apellido,
                'telefono': jefe_cocina.telefono,
                'fecha': jefe_cocina.fecha_registro
            })

        # Agregar los datos de los motorizados
        for motorizado in motorizados:
            empleados_data.append({
                'sucursal': motorizado.id_sucursal.snombre,
                'ciudad': motorizado.id_sucursal.sdireccion,
                'nombre': motorizado.nombre,
                'apellido': motorizado.apellido,
                'telefono': motorizado.telefono,
                'fecha': motorizado.fecha_registro
            })

        return JsonResponse({'empleados': empleados_data})
    
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
def listar_empleados2(request, **kwargs):
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
        empleados = [
            {
                'id': j.id_cuenta.id_cuenta,
                'nombre': j.nombre,
                'apellido': j.apellido,
                'telefono': j.telefono,
                'tipo': 'X',
                'sucursal': j.id_sucursal.id_sucursal if j.id_sucursal else None
            } for j in jefes_cocina
        ] + [
            {
                'id': mo.id_cuenta.id_cuenta,
                'nombre': mo.nombre,
                'apellido': mo.apellido,
                'telefono': mo.telefono,
                'tipo': 'D',
                'sucursal': mo.id_sucursal.id_sucursal if mo.id_sucursal else None
            } for mo in motorizados
        ] + [
            {
                'id': a.id_cuenta.id_cuenta,
                'nombre': a.nombre,
                'apellido': a.apellido,
                'telefono': a.telefono,
                'tipo': 'A',
                'sucursal': a.id_sucursal.id_sucursal if a.id_sucursal else None
            } for a in administradores
        ] + [
            {
                'id': m.id_cuenta.id_cuenta,
                'nombre': m.nombre,
                'apellido': m.apellido,
                'telefono': m.telefono,
                'tipo': 'M',
                'sucursal': m.id_sucursal.id_sucursal if m.id_sucursal else None
            } for m in meseros
        ]

        return JsonResponse({'empleados': empleados})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)