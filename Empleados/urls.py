from django.urls import path
from .views import *

urlpatterns = [
    path('crear/', CrearUsuarioView.as_view(), name='crearempleado'),
    path('listar-empleados/<int:idsucursal>/', listar_empleados, name='listar_empleados'),
    path('editar-empleado/<str:tipo_empleado>/<int:empleado_id>/', EditarEmpleadoView.as_view(), name='editar_empleado'),
]