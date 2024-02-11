from django.shortcuts import render
from Inventario.models import Inventario
from Producto.models import *
from Proveedores.models import *
from Bodega.models import Bodegas
from django.views import View
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from decimal import Decimal 
from Proveedores.models import *
from datetime import datetime
import traceback
import json
from django.db import transaction
from Inventario.models import MovimientoInventario, DetalleMovimientoInventario
from Login.models import Cuenta

@method_decorator(csrf_exempt, name='dispatch')
class CrearInventario(View):
    @transaction.atomic
    def post(self, request, id_bodega, *args, **kwargs):
        try:
            with transaction.atomic():
            # Obtener datos del pedido desde el request
                id_proveedor = request.POST.get('id_proveedor')
                fecha_pedido = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                fecha_entrega_esperada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                observacion_pedido = request.POST.get('observacion_pedido')
                proveedor_instance = get_object_or_404(Proveedores, id_proveedor=id_proveedor)

                bodega_instance = get_object_or_404(Bodegas, id_bodega=id_bodega)
                idumfinal=None
                # Crear el pedido
                pedido = Pedidosproveedor.objects.create(
                    id_proveedor=proveedor_instance,
                    id_bodega=bodega_instance,
                    fechapedido=fecha_pedido,
                    fechaentregaesperada=fecha_entrega_esperada,
                    estado='P',
                    observacion=observacion_pedido
                )
                newmovimiento=MovimientoInventario.objects.create(
                    id_cuenta=Cuenta.objects.get(id_cuenta=1),
                    tipomovimiento='E'
                )
                
                detalles_pedido_raw = request.POST.get('detalles_pedido', '{}')

                detalles_pedido = json.loads(detalles_pedido_raw)
                # Iterar sobre los detalles del pedido
                for detalle_pedido_data in detalles_pedido['detalles_pedido']:
                    # Obtener datos del detalle del pedido desde el request
                    id_producto = detalle_pedido_data.get('id_producto')
                    id_componente = detalle_pedido_data.get('id_componente')
                    cantidad_pedido = detalle_pedido_data['cantidad_pedido']
                    print(cantidad_pedido)
                    costo_unitario = detalle_pedido_data['costo_unitario']
                    id_umid = detalle_pedido_data.get('id_um')
                    id_um= UnidadMedida.objects.get(idum=id_umid)
                    if id_producto and id_componente:
                        return JsonResponse({'error':'Debe ingresar solo un componente o un producto.'}, status=400)
                    if id_producto:
                        producto_instance = get_object_or_404(Producto, id_producto=id_producto)
                        componente_instance = None
                        idumfinal=producto_instance.id_um
                        if(producto_instance.id_um != id_um):
                            eum=EnsambleUnidadMedida.objects.get(idump=id_um,idumc=producto_instance.id_um)
                            if(eum):
                                cantidad_pedido = Decimal(cantidad_pedido) / eum.cantidadconversion
                            else:
                                return JsonResponse({'error':'No hay conversión para esa unidad de medida, intenta registrar en '+producto_instance.id_um.nombreum+'.'}, status=400)
                    elif id_componente:
                        componente_instance = get_object_or_404(Componente, id_componente=id_componente)
                        producto_instance = None
                        idumfinal=componente_instance.id_um
                        if(componente_instance.id_um != id_um):
                            eum=EnsambleUnidadMedida.objects.get(idump=componente_instance.id_um,idumc=id_um)#falla
                            if(eum):
                                cantidad_pedido = Decimal(cantidad_pedido) / eum.cantidadconversion

                            else:
                                return JsonResponse({'No hay conversión para esa unidad de medida, intenta registrar en '+componente_instance.id_um.nombreum+'.'}, status=400)

                    else:
                        raise ValueError('Debe ingresar un componente o un producto.')
                    detalle_pedido = Detallepedidoproveedor.objects.create(
                        id_pedidoproveedor=pedido,
                        id_producto=producto_instance,
                        id_componente=componente_instance,
                        cantidad=cantidad_pedido,
                        costounitario=costo_unitario,
                        id_um=id_um
                    )
                    newdetalle = DetalleMovimientoInventario.objects.create(
                        id_movimientoinventario = newmovimiento,
                        id_articulo = componente_instance,
                        id_producto = producto_instance,
                        cantidad = cantidad_pedido,
                        tipo = 'E'
                    )

                    # Actualizar el inventario
                    inventario, created = Inventario.objects.get_or_create(
                        id_bodega=bodega_instance,
                        id_producto=producto_instance,
                        id_componente=componente_instance,
                        id_um=idumfinal,
                        defaults={'cantidad_disponible': cantidad_pedido, 'costo_unitario': costo_unitario}
                    )

                    if not created:
                        # Si ya existe el registro en el inventario, actualiza la cantidad disponible y el costo unitario
                        inventario.cantidad_disponible += cantidad_pedido
                        inventario.costo_unitario = costo_unitario
                        inventario.save()

                return JsonResponse({'mensaje': 'Pedido y inventario creados con éxito'})
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class ListarInventario(View):
    def get(self, request, *args, **kwargs):
        try:
            inventario_list = Inventario.objects.all()
            inventario_data = []

            for inventario in inventario_list:
                inventario_data.append({
                    'id_inventario': inventario.id_inventario,
                    'id_bodega': inventario.id_bodega.id_bodega,
                    'id_producto': inventario.id_producto.id_producto if inventario.id_producto else None,
                    'id_componente': inventario.id_componente.id_componente if inventario.id_componente else None,
                    'costo_unitario': str(inventario.costo_unitario),
                    'id_um': inventario.id_um.idum if inventario.id_um else None,
                    'stock_minimo': str(inventario.stock_minimo),
                    'cantidad_disponible': str(inventario.cantidad_disponible),
                })

            return JsonResponse({'inventario': inventario_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class EditarInventario(View):
    def post(self, request, *args, **kwargs):
        try:
            id_inventario = kwargs.get('id_inventario')
            cantidad_aumentar = request.POST.get('cantidad_aumentar') 
            nuevo_stock_minimo = request.POST.get('nuevo_stock_minimo')
            nuevo_costo_unitario = request.POST.get('nuevo_costo_unitario')

            inventario = get_object_or_404(Inventario, id_inventario=id_inventario)

            if cantidad_aumentar:
                cantidad_aumentar = Decimal(cantidad_aumentar)
                inventario.cantidad_disponible += cantidad_aumentar

            if nuevo_stock_minimo:
                nuevo_stock_minimo = Decimal(nuevo_stock_minimo)
                inventario.stock_minimo = nuevo_stock_minimo

            if nuevo_costo_unitario:
                nuevo_costo_unitario = Decimal(nuevo_costo_unitario)
                inventario.costo_unitario = nuevo_costo_unitario

            inventario.save()

            return JsonResponse({'mensaje': 'Inventario actualizado con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
