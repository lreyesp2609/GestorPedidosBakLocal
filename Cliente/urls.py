from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('actualizar_cliente/', ActualizarClienteView.as_view(), name='actualizar_cliente'),
    path('actualizar_cliente/<int:id_cliente>/', EditarCliente.as_view(), name='actualizar_cliente'),
    path('ver_clientes/', VerClientesView.as_view(), name='ver_clientes'),
    path('realizar_pedido/<int:id_cuenta>/', RealizarPedidoView.as_view(), name='realizar_pedido'),
    path('cliente/<int:id_cuenta>/pedidos/<int:id_pedido>/', ver_factura_cliente, name='ver_factura_cliente'),
    path('obtener_pedido/<int:id_cuenta>/', obtenerPedidos.as_view(), name='obtener_pedidos'),
    path('obtener_pedido2/', obtenerPedidos2.as_view(), name='obtener_pedidos2'),
    path('actualizar_pedido/<int:id_pedido>/', CambiarEstadoPedidos.as_view(), name='actualizar_pedido'),
    path('actualizar_pago/<int:id_pedido>/', CambiarEstadoPagos.as_view(), name='actualizar_pago'),
    path('verificar_pedido_validado/<int:id_factura>/', verificar_pedido_validado, name='verificar_pedido_validado'),
]

