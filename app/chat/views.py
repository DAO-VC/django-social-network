from django.db.models import Q
from rest_framework import generics

from chat.models import Room
from chat.serializers import (
    CreateRoomSerializer,
    RoomDetailSerializer,
    RoomListSerializer,
    ReadAllMessageSerializer,
)


class StartNewChat(generics.CreateAPIView):
    """Представление создания нового чата"""

    queryset = Room.objects.all()
    serializer_class = CreateRoomSerializer


class RetrieveChat(generics.RetrieveDestroyAPIView):
    """Детальное представление чата"""

    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer


class MyChatsList(generics.ListAPIView):
    """Список всех чатов пользователя"""

    serializer_class = RoomListSerializer

    def get_queryset(self):
        return Room.objects.filter(
            Q(author=self.request.user) | Q(receiver=self.request.user)
        )


class ReadAllMessage(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = ReadAllMessageSerializer
    http_method_names = ["put"]
