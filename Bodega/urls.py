from django.urls import path
from .views import *

urlpatterns = [
    path('crear/', CrearBodegaView.as_view(), name='crear_bodega'),
    path('listar/', ListarBodegasView.as_view(), name='listar_bodegas'),
    path('editar/<int:bodega_id>/', EditarBodegaView.as_view(), name='editar_bodega')
]
