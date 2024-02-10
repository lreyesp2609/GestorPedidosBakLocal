from django.urls import path
from .views import *

urlpatterns = [
    path('crear_proveedor/', CrearProveedor.as_view(), name='crear_proveedor'),
    path('editar_proveedor/<int:proveedor_id>/', EditarProveedor.as_view(), name='editar_proveedor'),
    path('listar_proveedor/', ListarProveedores.as_view(), name='listar_proveedor'),
]