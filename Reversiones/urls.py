from django.urls import path
from .views import pagina_vacia

urlpatterns = [
    path('', pagina_vacia, name='pagina_vacia'),
]
