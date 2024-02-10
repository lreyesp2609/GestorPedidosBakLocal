from django.urls import path
from .views import *
DetallesHorarioView
urlpatterns = [
    path('CrearHorarioSucursal/', CrearHorarioSucursal.as_view(), name='CrearHorarioSucursal'),
    path('get/<int:id_horario>', DetallesHorarioView.as_view(), name='DetallesHorarioView'),
    path('edit/<int:id_horario>', EditarHorarioSucursal.as_view(), name='EditarHorarioSucursal'),
    path('CrearHorarioProducto/', CrearHorarioProducto.as_view(), name='CrearHorarioProducto'),
]