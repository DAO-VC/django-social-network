from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from django.db.utils import IntegrityError
from chat.models import Message, Room, ChatNotification
from core.models import User
from core.serializers import UserBaseSerializer
from image.serializers import ImageSerializer, FileSerializer
from offer.models.offer_candidate import CandidateStartup
from offer.serializers.candidate import CandidateStartupBaseSerializer
from profiles.models.investor import Investor
from profiles.models.professional import Professional
from profiles.models.startup import Startup
from profiles.serializers.investor import InvestorChatSerializer
from profiles.serializers.professional import ProfessionalInWorkTeamSerializer
from profiles.serializers.startup import StartupToArticleSerializer
from vacancy.models.candidate import Candidate
from django.contrib.contenttypes.models import ContentType

from vacancy.models.workteam import WorkTeam
from vacancy.serializers.candidate import CandidateBaseSerializer
from vacancy.serializers.workteam import WorkTeamBaseSerializer


class MessageSerializer(serializers.ModelSerializer):
    """Сериализатор сообщений"""

    images = ImageSerializer(many=True, read_only=True)
    files = FileSerializer(many=True, read_only=True)

    class Meta:
        model = Message
        exclude = ("room",)


# class RoomDetailSerializer(serializers.ModelSerializer,RoomListSerializer):
#     """Сериализатор комнаты/чаты"""
#
#     author = UserBaseSerializer(read_only=True)
#     receiver = UserBaseSerializer(read_only=True)
#     messages = MessageSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Room
#         fields = ["id", "author", "receiver", "messages"]


class CreateRoomSerializer(serializers.ModelSerializer):
    """Сериализатор создания чата/комнаты"""

    author = UserBaseSerializer(read_only=True)
    receiver = UserBaseSerializer(read_only=True)
    receiver_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Room
        fields = "__all__"

    def create(self, validated_data):
        current_user = self.context.get("request").user
        receiver_id = validated_data.pop("receiver_id")
        receiver = get_object_or_404(User, pk=receiver_id)

        # if Room.objects.filter(
        #         Q(author=current_user, receiver=receiver)
        #         | Q(author=receiver, receiver=current_user)
        # ).exists():
        #     raise ValidationError("This chat is already exist")

        instance = Room.objects.create(author=current_user, receiver=receiver)
        return instance


class RoomListSerializer(serializers.ModelSerializer):
    """Базовый сериализатор комнаты"""

    author_object = serializers.SerializerMethodField(read_only=True)
    # receiver_object = serializers.SerializerMethodField(read_only=True)
    last_message = serializers.SerializerMethodField(read_only=True)
    count_unread_messages = serializers.SerializerMethodField(read_only=True)
    receiver_info = SerializerMethodField(read_only=True)

    def get_author_object(self, instance: Room):
        if instance.author.profile == User.UserProfile.STARTUP:
            return StartupToArticleSerializer(
                Startup.objects.filter(owner__id=instance.author.id).first()
            ).data
        if instance.author.profile == User.UserProfile.INVESTOR:
            return InvestorChatSerializer(
                Investor.objects.filter(owner__id=instance.author.id).first()
            ).data
        if instance.receiver.profile == User.UserProfile.PROFESSIONAL:
            return ProfessionalInWorkTeamSerializer(
                Professional.objects.filter(owner__id=instance.author.id).first()
            ).data

    # def get_receiver_object(self, instance: Room):
    #     if instance.receiver.profile == User.UserProfile.STARTUP:
    #         return StartupToArticleSerializer(
    #             Startup.objects.filter(owner__id=instance.author.id).first()
    #         ).data
    #     if instance.receiver.profile == User.UserProfile.INVESTOR:
    #         return InvestorChatSerializer(
    #             Investor.objects.filter(owner__id=instance.author.id).first()
    #         ).data
    #     if instance.receiver.profile == User.UserProfile.PROFESSIONAL:
    #         return ProfessionalInWorkTeamSerializer(
    #             Professional.objects.filter(owner__id=instance.author.id).first()
    #         ).data

    def get_last_message(self, instance: Room):
        return MessageSerializer(
            Message.objects.filter(room_id=instance.id).first()
        ).data

    def get_count_unread_messages(self, instance: Room):
        return (
            Message.objects.filter(room_id=instance.id, is_read=False)
            .exclude(author__id=self.context["request"].user.id)
            .count()
        )

    def get_receiver_info(self, instance: Room):
        if isinstance(instance.content_object, Candidate):
            return CandidateBaseSerializer(instance.content_object).data
        if isinstance(instance.content_object, CandidateStartup):
            return CandidateStartupBaseSerializer(instance.content_object).data
        if isinstance(instance.content_object, WorkTeam):
            return WorkTeamBaseSerializer(instance.content_object).data

    class Meta:
        model = Room
        fields = [
            "id",
            "author",
            "receiver",
            "author_object",
            # "receiver_object",
            "created_at",
            "last_message",
            "count_unread_messages",
            "receiver_info",
        ]


class NotificationSerializer(serializers.ModelSerializer):
    """Базовый сериализатор уведомления"""

    class Meta:
        model = ChatNotification
        fields = "__all__"


class RoomDetailSerializer(RoomListSerializer):
    """Сериализатор комнаты/чаты"""

    author = UserBaseSerializer(read_only=True)
    receiver = UserBaseSerializer(read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    # receiver_info = SerializerMethodField(read_only=True)

    class Meta:
        model = Room
        fields = [
            "id",
            "author",
            "receiver",
            "author_object",
            # "receiver_object",
            "messages",
            "count_unread_messages",
            "receiver_info",
        ]

    # def get_receiver_info(self, instance: Room):
    #     if isinstance(instance.content_object, Candidate):
    #         return CandidateBaseSerializer(instance.content_object).data


class ReadAllMessageSerializer(serializers.ModelSerializer):
    def update(self, instance: Room, validated_data):
        user = self.context["request"].user
        messages = Message.objects.filter(room_id=instance.id).exclude(
            author__id=user.id
        )
        for message in messages:
            message.is_read = True
            message.save()
        return super().update(instance, validated_data)

    class Meta:
        model = Room
        exclude = ["id", "author", "receiver", "created_at"]


class BanUserSerializer(serializers.ModelSerializer):
    def update(self, instance: User, validated_data):
        # user = self.context["request"].user
        # if instance in user.user_banned_list.all():
        #     raise ValidationError("The user is already in the ban list")
        # user.user_banned_list.add(instance)
        user = self.context["request"].user
        user.get_ban_user(instance)
        return super().update(instance, validated_data)

    class Meta:
        model = User

        exclude = (
            "password",
            "last_login",
            "is_superuser",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "date_joined",
            "email",
            "phone",
            "code",
            "username",
            "is_onboarding",
            "profile",
            "online",
            "permissions",
            "groups",
            "user_permissions",
            "users_banned_list",
            "spam_count",
        )


class StartupChatCreateSerializer(serializers.ModelSerializer):
    author = UserBaseSerializer(read_only=True)
    receiver = UserBaseSerializer(read_only=True)
    receiver_info = SerializerMethodField(read_only=True)

    def create(self, validated_data):
        candidate = get_object_or_404(
            Candidate, pk=self.context.get("view").kwargs.get("pk")
        )
        author = self.context["request"].user
        receiver = get_object_or_404(User, pk=candidate.professional_id.owner.id)
        content_type = ContentType.objects.get_for_model(candidate)
        try:
            instance = Room.objects.create(
                author=author,
                receiver=receiver,
                content_type=content_type,
                object_id=candidate.id,
                status=Room.ChatStatus.NEW,
            )
        except IntegrityError:
            obj = Room.objects.filter(
                author_id=self.context["request"].user,
                receiver_id=receiver,
                object_id=candidate.id,
            ).first()
            print(obj)
            raise ValidationError(f"This chat is already exist : id {obj.id} ")
        return instance

    class Meta:
        model = Room
        # fields = "__all__"
        exclude = ["object_id", "content_type"]

    def get_receiver_info(self, instance: Room):
        return CandidateBaseSerializer(instance.content_object).data


class InvestorChatCreateSerializer(serializers.ModelSerializer):
    author = UserBaseSerializer(read_only=True)
    receiver = UserBaseSerializer(read_only=True)
    receiver_info = SerializerMethodField(read_only=True)

    def create(self, validated_data):
        candidate = get_object_or_404(
            CandidateStartup, pk=self.context.get("view").kwargs.get("pk")
        )
        author = self.context["request"].user
        receiver = get_object_or_404(User, pk=candidate.startup_id.owner.id)
        content_type = ContentType.objects.get_for_model(candidate)
        try:
            instance = Room.objects.create(
                author=author,
                receiver=receiver,
                content_type=content_type,
                object_id=candidate.id,
                status=Room.ChatStatus.NEW,
            )
        except IntegrityError:
            obj = Room.objects.filter(
                author_id=self.context["request"].user,
                receiver_id=receiver,
                object_id=candidate.id,
            ).first()
            raise ValidationError(f"This chat is already exist : id {obj.id} ")
        return instance

    class Meta:
        model = Room
        # fields = "__all__"
        exclude = ["object_id", "content_type"]

    def get_receiver_info(self, instance: Room):
        return CandidateStartupBaseSerializer(instance.content_object).data


class ChangeRoomStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ["status"]


class StartupWorkteamRoomSerializer(serializers.ModelSerializer):
    author = UserBaseSerializer(read_only=True)
    receiver = UserBaseSerializer(read_only=True)
    receiver_info = SerializerMethodField(read_only=True)

    def create(self, validated_data):
        startup = get_object_or_404(Startup, owner=self.context["request"].user)
        team_member = get_object_or_404(
            startup.work_team.all(), pk=self.context.get("view").kwargs.get("pk")
        )
        content_type = ContentType.objects.get_for_model(team_member)

        try:
            instance = Room.objects.create(
                author=self.context["request"].user,
                receiver=team_member.candidate_id.professional_id.owner,
                content_type=content_type,
                object_id=team_member.id,
                status=Room.ChatStatus.NEW,
            )
        except IntegrityError:
            obj = Room.objects.filter(
                author_id=self.context["request"].user,
                receiver_id=team_member.candidate_id.professional_id.owner.id,
                object_id=team_member.id,
            ).first()
            raise ValidationError(f"This chat is already exist : id {obj.id} ")
        return instance

    def get_receiver_info(self, instance: Room):
        return WorkTeamBaseSerializer(instance.content_object).data

    class Meta:
        model = Room
        # fields = "__all__"
        exclude = ["object_id", "content_type"]


class ProfessionalToStartupRoomSerializer(serializers.ModelSerializer):
    author = UserBaseSerializer(read_only=True)
    receiver = UserBaseSerializer(read_only=True)
    receiver_info = SerializerMethodField(read_only=True)

    def create(self, validated_data):
        queryset = Candidate.objects.select_related(
            "professional_id", "vacancy_id"
        ).filter(
            professional_id__owner_id=self.context["request"].user,
            accept_status=Candidate.AcceptStatus.IN_THE_TEAM,
        )
        candidate = get_object_or_404(
            queryset, pk=self.context.get("view").kwargs.get("pk")
        )
        content_type = ContentType.objects.get_for_model(candidate)

        try:
            instance = Room.objects.create(
                author=self.context["request"].user,
                receiver=candidate.vacancy_id.company_id.owner,
                content_type=content_type,
                object_id=candidate.id,
                status=Room.ChatStatus.NEW,
            )
        except IntegrityError:
            obj = Room.objects.filter(
                author_id=self.context["request"].user,
                receiver_id=candidate.vacancy_id.company_id.owner.id,
                object_id=candidate.id,
            ).first()
            raise ValidationError(f"This chat is already exist : id {obj.id} ")
        return instance

    def get_receiver_info(self, instance: Room):
        return CandidateBaseSerializer(instance.content_object).data

    class Meta:
        model = Room
        # fields = "__all__"
        exclude = ["object_id", "content_type"]


class InvestorToConfirmedStartupRoomSerializer(serializers.ModelSerializer):
    author = UserBaseSerializer(read_only=True)
    receiver = UserBaseSerializer(read_only=True)
    receiver_info = SerializerMethodField(read_only=True)

    def create(self, validated_data):
        queryset = CandidateStartup.objects.filter(
            offer_id__investor_id__owner=self.context["request"].user,
            accept_status=CandidateStartup.AcceptStatus.ACCEPT,
        )
        candidate = get_object_or_404(
            queryset, pk=self.context.get("view").kwargs.get("pk")
        )
        content_type = ContentType.objects.get_for_model(candidate)

        try:
            instance = Room.objects.create(
                author=self.context["request"].user,
                receiver=candidate.startup_id.owner,
                content_type=content_type,
                object_id=candidate.id,
                status=Room.ChatStatus.NEW,
            )
        except IntegrityError:
            obj = Room.objects.filter(
                author_id=self.context["request"].user,
                receiver_id=candidate.startup_id.owner.id,
                object_id=candidate.id,
            ).first()
            raise ValidationError(f"This chat is already exist : id {obj.id} ")
        return instance

    def get_receiver_info(self, instance: Room):
        return CandidateStartupBaseSerializer(instance.content_object).data

    class Meta:
        model = Room
        # fields = "__all__"
        exclude = ["object_id", "content_type"]


class StartupToInvestorRoomSerializer(serializers.ModelSerializer):
    author = UserBaseSerializer(read_only=True)
    receiver = UserBaseSerializer(read_only=True)
    receiver_info = SerializerMethodField(read_only=True)

    def create(self, validated_data):
        queryset = CandidateStartup.objects.filter(
            startup_id__owner=self.context["request"].user,
            accept_status=CandidateStartup.AcceptStatus.ACCEPT,
        )
        candidate = get_object_or_404(
            queryset, pk=self.context.get("view").kwargs.get("pk")
        )
        content_type = ContentType.objects.get_for_model(candidate)

        try:
            instance = Room.objects.create(
                author=self.context["request"].user,
                receiver=candidate.offer_id.investor_id.owner,
                content_type=content_type,
                object_id=candidate.id,
                status=Room.ChatStatus.NEW,
            )
        except IntegrityError:
            obj = Room.objects.filter(
                author_id=self.context["request"].user,
                receiver_id=candidate.offer_id.investor_id.owner.id,
                object_id=candidate.id,
            ).first()
            raise ValidationError(f"This chat is already exist : id {obj.id} ")
        return instance

    def get_receiver_info(self, instance: Room):
        return CandidateStartupBaseSerializer(instance.content_object).data

    class Meta:
        model = Room
        # fields = "__all__"
        exclude = ["object_id", "content_type"]


class SpamUserSerializer(serializers.ModelSerializer):
    def update(self, instance: User, validated_data):
        user = self.context["request"].user
        user.get_ban_user(instance)
        instance.increase_spam_count()
        return super().update(instance, validated_data)

    class Meta:
        model = User

        exclude = (
            "password",
            "last_login",
            "is_superuser",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "date_joined",
            "email",
            "phone",
            "code",
            "username",
            "is_onboarding",
            "profile",
            "online",
            "permissions",
            "groups",
            "user_permissions",
            "users_banned_list",
            "spam_count",
        )
