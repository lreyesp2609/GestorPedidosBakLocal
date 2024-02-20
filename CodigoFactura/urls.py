# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('crear_codigosri/<int:id_cuenta>/', crear_codigosri, name='crear_codigosri'),
    path('crear_codigoautorizacion/<int:id_cuenta>/', crear_codigoautorizacion, name='crear_codigoautorizacion'),

    # Otras URLs de tu aplicación
]
