from django.urls import path
from .views import *

urlpatterns = [
    path('crear/', CrearMesa.as_view(), name='crearmesa'),
    path('ver_mesas/', MostrarMesas.as_view(), name='MostrarMesas'),
    path('editar_mesa/<int:id_mesa>/', EditarMesa.as_view(), name='editar_mesa'),
    path('crear_reservacion/', CrearReservacion.as_view(), name='crearreservacion'),
    path('listar_reservaciones/', ListarReservaciones.as_view(), name='listar_reservaciones'),
    path('editar_reservacion/<int:id_reservacion>/', EditarReservacion.as_view(), name='editar_reservacion'),
]
