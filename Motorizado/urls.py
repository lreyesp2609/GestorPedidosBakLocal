from django.urls import path
from .views import *

urlpatterns = [
    path('pedidos/domicilio/', pedidos_domicilio, name='pedidos_domicilio'),
    path('pedidos/aceptar-pedido/', aceptar_pedido, name='aceptar_pedido'),
    path('pedidos/entregar-pedido/', entregar_pedido, name='entregar_pedido'),
    path('pedidos/caja-diaria/<int:id_motorizado>/', caja_diaria, name='caja_diaria'),

]