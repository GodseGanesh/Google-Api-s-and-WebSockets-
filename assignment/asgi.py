import os
import django



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assignment.settings')
django.setup()


import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from chat.routing import websocket_urlpatterns
from chat.websocket_config.jwt_middleware import JwtMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "yourproject.settings")
django.setup()

application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        JwtMiddleware(
            URLRouter(websocket_urlpatterns)
        )
    )
})# asgi.py
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from chat.routing import websocket_urlpatterns  
from chat.websocket_config.jwt_middleware import JwtMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings')
django.setup()


django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,  
    "websocket": JwtMiddleware(
        URLRouter(websocket_urlpatterns)  
    ),
})




