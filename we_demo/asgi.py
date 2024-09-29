"""
ASGI config for we_demo project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from channels import routing
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from we_demo import routings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'we_demo.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter(routings.websocket_urlpatterns),  # 1.创建routings(相当于创建urls.py); 2.创建consumers(相当于创建views.py)
})