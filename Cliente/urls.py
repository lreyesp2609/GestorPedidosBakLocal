from django.urls import path
from .views import ActualizarClienteView, EditarCliente, VerClientesView, RealizarPedidoView, ver_factura_cliente,pedidos_del_cliente 

urlpatterns = [
    path('actualizar_cliente/', ActualizarClienteView.as_view(), name='actualizar_cliente'),
    path('actualizar_cliente/<int:id_cliente>/', EditarCliente.as_view(), name='actualizar_cliente'),
    path('ver_clientes/', VerClientesView.as_view(), name='ver_clientes'),
    path('realizar_pedido/<int:id_cuenta>/', RealizarPedidoView.as_view(), name='realizar_pedido'),
    path('cliente/<int:id_cliente>/pedidos/<int:id_pedido>/', ver_factura_cliente, name='ver_factura_cliente'),
    path('cliente/<int:id_usuario>/pedidos/', pedidos_del_cliente.as_view(), name='pedidos_del_cliente'),

]
