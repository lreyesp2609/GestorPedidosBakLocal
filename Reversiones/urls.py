from django.urls import path
from .views import GuardarReversionMovimiento

urlpatterns = [
    path('reversion/<int:movimiento_id>/', GuardarReversionMovimiento.as_view(), name='guardar_reversion_movimiento'),
]