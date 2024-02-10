from django.urls import path
from .views import CrearCompra

urlpatterns = [
    path('crear_compra/', CrearCompra.as_view(), name='crear_compra'),
]
