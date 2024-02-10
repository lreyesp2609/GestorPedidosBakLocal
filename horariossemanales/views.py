from django.shortcuts import render
from .models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from Sucursal.models import Sucursales
from Producto.models import Producto
from Producto.models import HorarioProducto
from django.views import View
from django.db import transaction
from django.http import JsonResponse

@method_decorator(csrf_exempt, name='dispatch')
class CrearHorarioSucursal(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            # Obtener datos del cuerpo de la solicitud
            nombreh = request.POST.get('nombreh', '')
            hordescripcion = request.POST.get('hordescripcion', '')
            idsucursal = request.POST.get('idsucursal', '')
            detalle = json.loads(request.POST.get('detalle', '[]'))
            sucursal= Sucursales.objects.get(id_sucursal=idsucursal)
            sucursal.id_horarios=Horariossemanales.objects.create(
                nombreh=nombreh,
                hordescripcion=hordescripcion,
                tipohorario='A',
            )
            sucursal.save()
            
            for det in detalle['Detalles']:
                id_horarios = sucursal.id_horarios
                print(id_horarios)
                print(f"hla uwu")
                dia = det['dia']
                hora_inicio = det['hora_inicio']
                hora_fin=det['hora_fin']
                DetalleHorariosSemanales.objects.create(
                    id_horarios = id_horarios,
                    dia =dia,
                    horainicio = hora_inicio,
                    horafin = hora_fin
                )
            return JsonResponse({'mensaje': 'Horario agregado con exito'})
        
        except Exception as e:
            print( str(e))
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class DetallesHorarioView(View):
    def get(self, request, *args, **kwargs):
        try:
            id_horario = kwargs.get('id_horario')
            detalles = DetalleHorariosSemanales.objects.filter(id_horarios=id_horario)
            detalles_list = [{'dia': nombre_dia(detalle.dia), 'hora_inicio': detalle.horainicio, 'hora_fin': detalle.horafin} for detalle in detalles]
            return JsonResponse({'detalles': detalles_list})
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
def nombre_dia(dia):
    if dia=='L':
        return 'Lunes'
    if dia=='M':
        return 'Martes'
    if dia=='X':
        return 'Miercoles'
    if dia=='J':
        return 'Jueves'
    if dia=='V':
        return 'Viernes'
    if dia=='S':
        return 'Sabado'
    if dia=='D':
        return 'Domingo'
@method_decorator(csrf_exempt, name='dispatch')
class EditarHorarioSucursal(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            id_horario = kwargs.get('id_horario')
            detalles_actuales = DetalleHorariosSemanales.objects.filter(id_horarios=id_horario)           
            detalles_nuevos = json.loads(request.POST.get('detalle', '[]'))
            id_horarios = Horariossemanales.objects.get(id_horarios=id_horario)
            i=0
            for det in detalles_nuevos['Detalles']:
                if i < len(detalles_actuales):
                    detalle_actual = detalles_actuales[i]
                    detalle_actual.dia = det['dia']
                    detalle_actual.horainicio = det['hora_inicio']
                    detalle_actual.horafin = det['hora_fin']
                    detalle_actual.save()
                    
                else:
                    DetalleHorariosSemanales.objects.create(
                        id_horarios=id_horarios,
                        dia=det['dia'],
                        horainicio=det['hora_inicio'],
                        horafin=det['hora_fin']
                    )
                i=i+1
            return JsonResponse({'mensaje': 'Horario actualizado con éxito'})
        
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class CrearHorarioProducto(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            # Obtener datos del cuerpo de la solicitud
            nombreh = request.POST.get('nombreh', '')
            hordescripcion = request.POST.get('hordescripcion', '')
            idsucursal = request.POST.get('idsucursal', '')
            idproducto = request.POST.get('idproducto', '')
            detalle = json.loads(request.POST.get('detalle', '[]'))
            sucursal= Sucursales.objects.get(id_sucursal=idsucursal)
            Productox= Producto.objects.get(id_producto=idproducto)
            horariosem=Horariossemanales.objects.create(
                    nombreh=nombreh,
                    hordescripcion=hordescripcion,
                    tipohorario='P',
                )
            HorarioProductoz=HorarioProducto.objects.create(
                id_horarios = horariosem,
                id_sucursal = sucursal,
                id_producto = Productox
            )

            HorarioProductoz.save()
            
            for det in detalle['Detalles']:
                id_horarios = HorarioProductoz.id_horarios
                print(id_horarios)
                print(f"hla uwu")
                dia = det['dia']
                hora_inicio = det['hora_inicio']
                hora_fin=det['hora_fin']
                DetalleHorariosSemanales.objects.create(
                    id_horarios = id_horarios,
                    dia =dia,
                    horainicio = hora_inicio,
                    horafin = hora_fin
                )
            return JsonResponse({'mensaje': 'Horario agregado con exito'})
        
        except Exception as e:
            print( str(e))
            return JsonResponse({'error': str(e)}, status=400)