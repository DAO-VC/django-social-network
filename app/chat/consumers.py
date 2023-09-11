import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
import base64
import secrets
from django.core.files.base import ContentFile
from chat.models import Room, Message, ChatNotification
from chat.serializers import MessageSerializer
from core.models import User
from image.models import Image, File


class ChatConsumer(AsyncWebsocketConsumer):
    """Сущность потребителя для реализации realtime чата.
    room_name - id созданной комнаты"""

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        attachments = text_data_json.get("attachment")
        if attachments:
            images, files = await self.save_images(attachments)
            result = await self.save_message(text_data_json["message"])
            result = await self.add_image_to_message(result, images, files)
        else:

            result: Message = await self.save_message(text_data_json["message"])

        serializer = MessageSerializer(await self.get_object(result))

        return_dict = {
            "type": "chat_message",
            # 'message': text_data_json['message'],
            "message": serializer.data,
            "username": self.scope["user"].email,
        }

        await self.channel_layer.group_send(
            self.room_group_name,
            return_dict,
        )

    async def chat_message(self, event):
        message = event["message"]
        # user = event["username"]

        await self.send(text_data=json.dumps({"message": message}, ensure_ascii=False))

    @database_sync_to_async
    def save_message(self, message):
        room = Room.objects.get(id=int(self.room_name))
        user = self.scope["user"]
        if (
            user in room.receiver.users_banned_list.all()
            or room.receiver in user.users_banned_list.all()
        ):
            instance = Message.objects.create(
                author=user,
                room=room,
                text=message,
                is_read=False,
                ban_status=True,
            )
            return instance

        instance = Message.objects.create(
            author=user, room=room, text=message, is_read=False, ban_status=False
        )
        if user.id == room.author.id:
            ChatNotification.objects.create(
                user=room.receiver,
                author=user,
                text=f"You have new message from {user}",
            )
        else:
            ChatNotification.objects.create(
                user=room.author,
                author=room.receiver,
                text=f"You have new message from {room.receiver}",
            )

        return instance

    @database_sync_to_async
    def save_images(self, attachments):
        images = []
        files = []
        for attachment in attachments:
            file_str, file_ext = attachment["data"], attachment["format"]
            if file_ext == "pdf":
                file_data = ContentFile(
                    base64.b64decode(file_str),
                    name=f"{secrets.token_hex(8)}.{file_ext}",
                )
                instance = File.objects.create()
                instance.pdf.save(file_data.name, file_data)
                files.append(instance)
            else:
                file_data = ContentFile(
                    base64.b64decode(file_str),
                    name=f"{secrets.token_hex(8)}.{file_ext}",
                )
                instance = Image.objects.create()
                instance.image.save(file_data.name, file_data)
                images.append(instance)
        return images, files

    @database_sync_to_async
    def add_image_to_message(self, message: Message, images, files):
        for image in images:
            message.images.add(image)
        message.save()
        for file in files:
            message.files.add(file)
        message.save()
        return message

    @database_sync_to_async
    def get_object(self, obj):
        return (
            Message.objects.prefetch_related("images")
            .prefetch_related("files")
            .filter(id=obj.id)
        ).first()


class NotificationConsumer(AsyncWebsocketConsumer):
    """Сущность потребителя для реализации уведомлений приложения."""

    async def connect(self):
        my_id = self.scope["user"].id
        self.room_group_name = f"notify_{my_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def send_notification(self, event):
        data = json.loads(event.get("value"))
        count = data["count"]
        message = data["message"]
        notification = data["notification"]

        await self.send(
            text_data=json.dumps(
                {"count": count, "message": message, "notification": notification}
            )
        )

    async def chat_message(self, event):
        notifications_id = event["notifications_id"]
        username = event["username"]
        await self.send(
            text_data=json.dumps(
                {
                    "notifications_id": notifications_id,
                    "username": username,
                    "status": "all  notifications is read",
                },
                ensure_ascii=False,
            )
        )

    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        notifications_id = text_data_json["notifications_id"]
        for id in notifications_id:
            await self.read_notification(notif_id=id)
        return_dict = {
            "type": "chat_message",
            "notifications_id": notifications_id,
            "username": self.scope["user"].email,
        }
        await self.channel_layer.group_send(
            self.room_group_name,
            return_dict,
        )

    # @database_sync_to_async
    # def update_user_incr(self, user):
    #     User.objects.filter(pk=user.pk).update(online=F("online") + 1)
    #
    # @database_sync_to_async
    # def update_user_decr(self, user):
    #     User.objects.filter(pk=user.pk).update(online=F("online") - 1)
    #
    @database_sync_to_async
    def read_notification(self, notif_id):
        obj = ChatNotification.objects.filter(id=notif_id).first()
        obj.is_seen = True
        obj.save()


class OnlineStatusConsumer(AsyncWebsocketConsumer):
    """Сущность потребителя для реализации онлайн статуса пользователя."""

    async def connect(self):
        self.room_group_name = "user"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        email = data["email"]
        connection_type = data["type"]
        await self.change_online_status(email, connection_type)

    async def send_OnlineStatus(self, event):
        data = json.loads(event.get("value"))
        email = data["email"]
        online_status = data["status"]
        await self.send(
            text_data=json.dumps({"email": email, "online_status": online_status})
        )

    async def disconnect(self, message):
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    @database_sync_to_async
    def change_online_status(self, email, c_type):
        user = User.objects.get(email=email)

        if c_type == "open":
            user.online = True
            user.save()
        else:
            user.online = False
            user.save()


class MessagesConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        my_id = self.scope["user"].id
        self.room_group_name = f"message_{my_id}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None):
        text_data_json = json.loads(text_data)
        message_id = text_data_json["message_id"]

        message = await self.read_message(message_id=message_id)
        serializer = MessageSerializer(await self.get_object(message))
        return_dict = {
            "type": "chat_message",
            "message_id": serializer.data.get("id"),
            "read_status": serializer.data.get("is_read"),
            "chat_id": serializer.data.get("room"),
            # "username": self.scope["user"].email,
        }
        await self.channel_layer.group_send(
            self.room_group_name,
            return_dict,
        )

    async def chat_message(self, event):
        message_id = event["message_id"]
        # username = event["username"]
        read_status = event["read_status"]
        chat_id = event["chat_id"]
        await self.send(
            text_data=json.dumps(
                {
                    "message_id": message_id,
                    "read_status": read_status,
                    "chat_id": chat_id,
                    # "username": username,
                },
                ensure_ascii=False,
            )
        )

    async def send_message_status(self, event):
        data = json.loads(event.get("value"))
        message_id = data["message_id"]
        read_status = data["read_status"]
        chat_id = data["chat_id"]

        await self.send(
            text_data=json.dumps(
                {
                    "message_id": message_id,
                    "read_status": read_status,
                    "chat_id": chat_id,
                    # "username": username,
                },
                ensure_ascii=False,
            )
        )

    @database_sync_to_async
    def read_message(self, message_id):
        obj = Message.objects.filter(id=message_id).first()
        obj.is_read = True
        obj.save()
        return obj

    @database_sync_to_async
    def get_object(self, obj):
        return (
            Message.objects.prefetch_related("images")
            .prefetch_related("files")
            .filter(id=obj.id)
        ).first()
