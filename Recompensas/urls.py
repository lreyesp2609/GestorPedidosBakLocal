from django.urls import path
from .views import *

urlpatterns = [
    path('crear_recompensa_producto/', CrearRecompensaProducto.as_view(), name='crear_recompensa_producto'),
    path('crear_recompensa_combo/', CrearRecompensaCombo.as_view(), name='crear_recompensa_combo'),
    path('lista_recompensas_combo/', ListaRecompensasCombo.as_view(), name='lista_recompensas_combo'),
    path('lista_recompensas_producto/', ListaRecompensasProducto.as_view(), name='lista_recompensas_producto'),
    path('editar_recompensa_combo/<int:recompensa_combo_id>/', EditarRecompensaCombo.as_view(), name='editar_recompensa_combo'),
    path('editar_recompensa_producto/<int:recompensa_producto_id>/', EditarRecompensaProducto.as_view(), name='editar_recompensa_producto'),
    path('listar_productos_con_recompensas/', ListarProductosConRecompensas.as_view(), name='listar_productos_con_recompensas'),
    path('listar_combos_con_recompensas/', ListarCombosConRecompensas.as_view(), name='listar_combos_con_recompensas'),
    path('listar_combos_con_recompensas/', ListarCombosConRecompensas.as_view(), name='listar_combos_con_recompensas'),
    path('Restar_puntos/<int:id_usuario>/', RestarPuntos.as_view(), name='Restar_puntos'),
    path('Sumar_puntos/<int:id_usuario>/', SumarPuntos.as_view(), name='Sumar_puntos'),

]