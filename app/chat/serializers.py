from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from chat.models import Message, Room, ChatNotification
from core.models import User
from core.serializers import UserBaseSerializer


class MessageSerializer(serializers.ModelSerializer):
    """Сериализатор сообщений"""

    class Meta:
        model = Message
        exclude = ("room",)


class RoomDetailSerializer(serializers.ModelSerializer):
    """Сериализатор комнаты/чаты"""

    author = UserBaseSerializer(read_only=True)
    receiver = UserBaseSerializer(read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ["id", "author", "receiver", "messages"]


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

        if Room.objects.filter(
            Q(author=current_user, receiver=receiver)
            | Q(author=receiver, receiver=current_user)
        ).exists():
            raise ValidationError("This chat is already exist")

        instance = Room.objects.create(author=current_user, receiver=receiver)
        return instance


class RoomListSerializer(serializers.ModelSerializer):
    """Базовый сериализатор комнаты"""

    class Meta:
        model = Room
        fields = [
            "id",
            "author",
            "receiver",
        ]


class NotificationSerializer(serializers.ModelSerializer):
    """Базовый сериализатор уведомления"""

    class Meta:
        model = ChatNotification
        fields = "__all__"
