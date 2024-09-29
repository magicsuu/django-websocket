from django.urls import re_path

from app01 import consumers

websocket_urlpatterns = [
    # ws://127.0.0.1:8000/room/组号/
    re_path(r'room/(?P<group>\w+)/$', consumers.ChatConsumer.as_asgi()),
]