"""
ASGI config for progress_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'progress_project.settings')

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path 

from home import consumers

websocket_urlpatterns = [ 
    path('ws/order/<order_token>/', consumers.OrderProgressConsumer )
]

application = get_asgi_application()

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(URLRouter( 
        websocket_urlpatterns
    ))
})
