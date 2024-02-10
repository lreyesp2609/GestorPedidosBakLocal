from django.urls import path
from .views import *

urlpatterns = [
    path('tomar_pedido/', TomarPedido.as_view(), name='tomar_pedido'),
    path('ver_factura/<int:id_pedido>/', ver_factura, name='ver_factura'),
    #path('mesero/<int:id_mesero>/mesa/<int:id_mesa>/pedidos/', pedidos_del_mesero, name='pedidos_mesero_mesa'),
    path('mesero/mesa/<int:id_mesa>/pedidos/', pedidos_del_mesero, name='pedidos_mesero_mesa'),
]
