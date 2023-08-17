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
    StartupChatCreateSerializer,
    InvestorChatCreateSerializer,
    ChangeRoomStatusSerializer,
    StartupWorkteamRoomSerializer,
)
from core.models import User
from offer.permissions import OfferStartupCandidatesPermission
from vacancy.permissions import (
    StartupCandidateFavoriteRetrievePermission,
    StartupWorkTeamUpdatePermission,
)


class StartNewChat(generics.CreateAPIView):
    """Представление создания нового чата"""

    queryset = Room.objects.all()
    serializer_class = CreateRoomSerializer
    permission_classes = (IsAuthenticated,)


class StartupStartChat(generics.CreateAPIView):
    """Представление создания нового чата Startup / Professional"""

    # offer = get_object_or_404(Offer, pk=self.context.get("view").kwargs.get("pk"))
    queryset = Room.objects.all()
    serializer_class = StartupChatCreateSerializer
    permission_classes = (IsAuthenticated, StartupCandidateFavoriteRetrievePermission)


class InvestorStartChat(generics.CreateAPIView):
    """Представление создания нового чата Investor / Startup"""

    queryset = Room.objects.all()
    serializer_class = InvestorChatCreateSerializer
    permission_classes = (OfferStartupCandidatesPermission,)


class RetrieveChat(generics.RetrieveDestroyAPIView):
    """Детальное представление чата"""

    queryset = Room.objects.all()
    serializer_class = RoomDetailSerializer
    permission_classes = (RoomPermission,)


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


class ChangeRoomStatus(generics.UpdateAPIView):
    queryset = Room.objects.all()
    serializer_class = ChangeRoomStatusSerializer
    http_method_names = ["put"]
    permission_classes = (RoomPermission,)


class StartupWorkteamRoom(generics.CreateAPIView):
    """Представление создания нового чата Startup / WorkTeamMember"""

    queryset = Room.objects.all()
    serializer_class = StartupWorkteamRoomSerializer
    permission_classes = (IsAuthenticated, StartupWorkTeamUpdatePermission)
