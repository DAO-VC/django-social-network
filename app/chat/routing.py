from django.urls import path, re_path
from django.urls import path
from . import consumers
from .consumers import NotificationConsumer, OnlineStatusConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    path("/notify/", NotificationConsumer.as_asgi()),
    # path(r"ws/online/(?P<chat_id>\w+)/$", OnlineStatusConsumer.as_asgi()), ]
    path("/online/", OnlineStatusConsumer.as_asgi()),
]


# re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
#     path("ws/notify/", NotificationConsumer.as_asgi()),
#     # path(r"ws/online/(?P<chat_id>\w+)/$", OnlineStatusConsumer.as_asgi()), ]
#     path("ws/online/", OnlineStatusConsumer.as_asgi()),
