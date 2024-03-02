from django.urls import path
from .views import ListarSucursalReporte, SucursalesListView, Crearsucursal,sucursalExist,actdesSucursal,Editarubicacion,cargarSucursal,EditarSucursal,crearGeosector

urlpatterns = [
    path('sucusarleslist/', SucursalesListView.as_view(), name='SucursalesListView'),
    path('crear/', Crearsucursal.as_view(), name='Crearsucursal'),
    path('sucursalExist/', sucursalExist.as_view(), name='sucursalExist'),
    path('actsucursal/', actdesSucursal.as_view(), name='actdesSucursal'),
    path('editarubicacion/', Editarubicacion.as_view(), name='Editarubicacion'),
    path('cargarSucursal/<int:id_sucursal>', cargarSucursal.as_view(), name='cargarSucursal'),
    path('EditarSucursal/<int:id_sucursal>', EditarSucursal.as_view(), name='EditarSucursal'),
    path('crearGeosector/', crearGeosector.as_view(), name='crearGeosector'),
    path('listar-sucursales/', ListarSucursalReporte.as_view(), name='ListarSucursales'),
]