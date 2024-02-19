from django.urls import path
from .views import *

urlpatterns = [
    path('obtener_usuario/<int:id_usuario>/', ObtenerMeseroView.as_view(), name='obtener_mesero'),
    path('tomar_pedido/<int:id_cuenta>/', TomarPedido.as_view(), name='tomar_pedido'),
    path('ver_factura/<int:id_pedido>/', ver_factura, name='ver_factura'),
    path('mesero/<int:id_cuenta>/mesa/<int:id_mesa>/pedidos/', pedidos_del_mesero, name='pedidos_mesero_mesa'),
    path('pedidos/', ListaPedidos.as_view(), name='pedidos'),
    path('pedidoslocal/', TomarPedidoSinMesa.as_view(), name='tomar_pedido_2'),
]
