# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('crear_codigosri/<int:id_cuenta>/', crear_codigosri, name='crear_codigosri'),
    path('crear_codigoautorizacion/<int:id_cuenta>/', crear_codigoautorizacion, name='crear_codigoautorizacion'),
    path('validar_factura/<int:id_cuenta>/<int:id_factura>/', ValidarFactura.as_view(), name='validar_factura'),
    path('crear_punto/<int:id_cuenta>/', crear_punto_facturacion, name='crear_punto_facturacion'),
    path('validar_punto_facturacion/', ValidarPuntoFacturacion.as_view(), name='validar_punto_facturacion'),
    path('validar_permisos_factura/<int:id_cuenta>/', ValidarPermisosFactura.as_view(), name='validar_permisos_factura'),
    path('vercodigo/', VerCodigos.as_view(), name='vercodigo'),

    # Otras URLs de tu aplicación
]


