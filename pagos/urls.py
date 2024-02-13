from django.urls import path
from .views import *

urlpatterns = [
    path('creartipop/', CrearEditarTipopago.as_view(), name='creartipop'),
    path('tipodepagos/', ConsultarTipopago.as_view(), name='ConsultarTipopago'),
]