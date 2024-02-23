from django.urls import path
from .views import *
from . import views
urlpatterns = [
    path('crear/', CrearUsuarioView.as_view(), name='crearempleado'),
    path('listar-empleados/<int:idsucursal>/', listar_empleados, name='listar_empleados'),
    path('editar-empleado/<str:tipo_empleado>/<int:empleado_id>/', EditarEmpleadoView.as_view(), name='editar_empleado'),
    path('listar-empleados2/<int:idsucursal>/', listar_empleados2, name='listar_empleados2'),
    path('listar-empleados-tipo/<int:idsucursal>/<str:tipo_empleado>/', views.listar_empleados_tipo),
    path('listar-empleados-tipo/<int:idsucursal>/', views.listar_empleados_tipo),
    path('listar-empleados-tipo/', views.listar_todos_los_empleados, name='listar_todos_los_empleados'),
]