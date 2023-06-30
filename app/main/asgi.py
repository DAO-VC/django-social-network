import os
from channels_auth_token_middlewares.middleware import (
    QueryStringSimpleJWTAuthTokenMiddleware,
)

from chat import routing as chat_routing
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            QueryStringSimpleJWTAuthTokenMiddleware(
                URLRouter(chat_routing.websocket_urlpatterns)
            )
        ),
    }
)
