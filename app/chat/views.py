from django.db.models import Q
from rest_framework import generics

from chat.models import Room
from chat.serializers import (
    CreateRoomSerializer,
    RoomDetailSerializer,
    RoomListSerializer,
)


class StartNewChat(generics.CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = CreateRoomSerializer


class RetrieveChat(generics.RetrieveDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer


class MyChatsList(generics.ListAPIView):
    serializer_class = RoomListSerializer

    def get_queryset(self):
        return Room.objects.filter(
            Q(author=self.request.user) | Q(receiver=self.request.user)
        )
