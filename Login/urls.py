from django.urls import path
from .views import *

urlpatterns = [
    path('cerrar_sesion/', CerrarSesionView.as_view(), name='cerrar_sesion'),
    path('crear/', CrearUsuarioView.as_view(), name='crear_usuario'),
    path('iniciar_sesion/', IniciarSesionView.as_view(), name='iniciar_sesion'),
    path('editar_perfil/', EditarCliente.as_view(), name='editar_perfil'),
    path('prueba/', HomeView.as_view(), name='HomeView'),
    path('cuentaexist/', usuarioExist.as_view(), name='usuarioExist'),
    path('phoneExist/', telefonoExist.as_view(), name='telefonoExist'),
    path('DocumentExist/', DocumentExist.as_view(), name='DocumentExist'),
    path('rol/', VerificarRolView.as_view(), name='rol'),
    path('id/', DevolverUsuario.as_view(), name='usuario'),
    path('obtener_usuario/<int:id_usuario>/', ObtenerUsuariosView.as_view(), name='obtener_usuario_por_id'),
    path('obtener_cocinero/<int:id_cuenta>/', ObtenerCocinero.as_view(), name='ObtenerCocinero'),
    path('editar_usuario/<int:id_cuenta>/', EditarUsuariosView.as_view(), name='editar_usuario_por_id'),
    path('editar_ubicacion/<int:id_cuenta>/', EditarUbicacionCliente.as_view(), name='EditarUbicacionCliente'),

]