from django.urls import path
from .views import *

urlpatterns = [
    path('obtener_usuario/<int:id_usuario>/', ObtenerMeseroView.as_view(), name='obtener_mesero'),
    path('tomar_pedido/<int:id_cuenta>/', TomarPedido.as_view(), name='tomar_pedido'),
    path('ver_factura/<int:id_pedido>/', ver_factura, name='ver_factura'),
    path('mesero/<int:id_cuenta>/mesa/<int:id_mesa>/pedidos/', pedidos_del_mesero, name='pedidos_mesero_mesa'),
    path('pedidos/', ListaPedidos.as_view(), name='pedidos'),
    path('pedidoslocal/<int:id_cuenta>/', TomarPedidoSinMesa.as_view(), name='tomar_pedido_2'),
    path('listpedidos/', ListaPedidosMesero.as_view(), name='ListaPedidosMesero'),
    path('confirmarpedido/', ConfirmarPedido.as_view(), name='ConfirmarPedido'),
    path('listar_meseros/', ListaMeseros.as_view(), name='listar_meseros'),
    path('lista_facturas/', ListaFacturas.as_view(), name='lista_facturas'),
    path('crear_reverso_factura/<int:id_factura>/', CrearReversoFactura.as_view(), name='crear_reverso_factura'),
    path('validar_facturas/', FacturasValidadasReportes.as_view(), name='validar_facturas'),
    path('listapedidospagado/', ListaPedidosReportes.as_view(), name='listapagados'),
    path('listar_notas_credito/<int:id_notacredito>/', ListaNotasCredito.as_view(), name='listar_notas_credito'),
    path('detalle_factura/<int:id_factura>/', DetalleFacturaView.as_view(), name='detalle_factura'),
    path('lista_facturas_con_detalles/<int:id_factura>/', ListaFacturasConDetalles.as_view(), name='lista_facturas_con_detalles'),
]