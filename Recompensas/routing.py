from django.urls import re_path
from .consumers import ReclamarConsumer

websocket_urlpatterns = [
    re_path(r'ws/reclamar/$', ReclamarConsumer.as_asgi()),
]
