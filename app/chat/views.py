from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from chat.models import Room, Message
from chat.permissions import RoomPermission, RoomOwnerPermission, RoomPermissionNotObj
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
    ProfessionalToStartupRoomSerializer,
    InvestorToConfirmedStartupRoomSerializer,
    StartupToInvestorRoomSerializer,
    SpamUserSerializer,
)
from core.models import User
from core.permissions import StartupCreatePermission
from core.serializers import UserBaseSerializer
from image.models import Image, File
from image.serializers import ImageSerializer, FileSerializer
from offer.permissions import OfferStartupCandidatesPermission
from vacancy.permissions import (
    StartupCandidateFavoriteRetrievePermission,
    StartupWorkTeamUpdatePermission,
    ProfessionalMyApplicationsPermission,
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


class SpamUser(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = SpamUserSerializer
    http_method_names = ["put"]
    permission_classes = (IsAuthenticated,)


class BanUsersList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserBaseSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        instance: User = (
            User.objects.filter(id=self.request.user.id).first().users_banned_list.all()
        )
        return instance


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


class ProfessionalToStartupRoom(generics.CreateAPIView):
    """Представление создания нового чата Professional / Startup"""

    queryset = Room.objects.all()
    serializer_class = ProfessionalToStartupRoomSerializer
    permission_classes = (IsAuthenticated, ProfessionalMyApplicationsPermission)


class InvestorToConfirmedStartupRoom(generics.CreateAPIView):
    """Представление создания нового чата Investor / Startup"""

    queryset = Room.objects.all()
    serializer_class = InvestorToConfirmedStartupRoomSerializer
    permission_classes = (IsAuthenticated,)


class StartupToInvestorRoom(generics.CreateAPIView):
    """Представление создания нового чата Startup / Investor"""

    queryset = Room.objects.all()
    serializer_class = StartupToInvestorRoomSerializer
    permission_classes = (IsAuthenticated, StartupCreatePermission)


class AllRoomImages(generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = (RoomPermissionNotObj,)

    def get_queryset(self):
        messages = Message.objects.filter(
            room_id=self.kwargs.get("pk"), images__isnull=False
        )
        images = []
        for message in messages:
            for item in message.images.all():
                images.append(item)
        return images


class AllRoomFiles(generics.ListAPIView):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (RoomPermissionNotObj,)

    def get_queryset(self):
        messages = Message.objects.filter(
            room_id=self.kwargs.get("pk"), files__isnull=False
        )
        files = []
        for message in messages:
            for item in message.files.all():
                files.append(item)
        return files
