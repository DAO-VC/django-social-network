from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from chat.models import Room
from chat.permissions import RoomPermission, RoomOwnerPermission
from chat.serializers import (
    CreateRoomSerializer,
    RoomDetailSerializer,
    RoomListSerializer,
    ReadAllMessageSerializer,
    BanUserSerializer,
)
from core.models import User


class StartNewChat(generics.CreateAPIView):
    """Представление создания нового чата"""

    queryset = Room.objects.all()
    serializer_class = CreateRoomSerializer
    permission_classes = (IsAuthenticated,)


class RetrieveChat(generics.RetrieveDestroyAPIView):
    """Детальное представление чата"""

    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer
    permission_classes = (RoomOwnerPermission,)


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
    permission_classes = (RoomPermission,)


class BanUser(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = BanUserSerializer
    http_method_names = ["put"]
    permission_classes = (IsAuthenticated,)
