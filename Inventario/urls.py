from django.urls import path
from .views import * 

urlpatterns = [
    path('crearinventario/<int:id_bodega>/', CrearInventario.as_view(), name='crearinventario'),
    path('verinventario/', ListarInventario.as_view(), name='verinventario'),
    path('editar/<int:id_inventario>/', EditarInventario.as_view(), name='editar_inventario'),
    path('listar_movimientos_inventario/', ListarMovimientosInventario.as_view(), name='listar_movimientos_inventario'),
    path('crear_movimiento_reversion/<int:id_movimiento_origen>/', CrearMovimientoReversion.as_view(), name='crear_movimiento_reversion'),
]
