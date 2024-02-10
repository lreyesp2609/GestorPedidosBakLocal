from django.urls import re_path
from .consumers import HolaMundoConsumer

websocket_urlpatterns = [
    re_path(r'ws/hola_mundo/$', HolaMundoConsumer.as_asgi()),
]