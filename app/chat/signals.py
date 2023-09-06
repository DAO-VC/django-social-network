import json
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from chat.models import ChatNotification, Room, Message
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from chat.serializers import NotificationSerializer


@receiver(post_save, sender=ChatNotification)
def send_notification(sender, instance: ChatNotification, created, **kwargs):
    """Базовый сигнал модели Уведомление"""
    if created:
        channel_layer = get_channel_layer()
        notification_obj = ChatNotification.objects.filter(
            is_seen=False, user=instance.user
        ).count()
        user_id = str(instance.user.id)
        serializer = NotificationSerializer(instance)
        data = {
            "count": notification_obj,
            "message": instance.text,
            "notification": serializer.data,
        }

        channel_name = f"notify_{user_id}"
        async_to_sync(channel_layer.group_send)(
            channel_name, {"type": "send_notification", "value": json.dumps(data)}
        )


@receiver(post_save, sender=Room)
def send_start_room_notification(sender, instance: Room, created, **kwargs):
    """ "Сигнал создания нового чата"""
    if created:
        author = instance.author
        receiver = instance.receiver
        ChatNotification.objects.create(
            user=receiver,
            author=author,
            text=f"You have new chat with {instance.author}",
        )


@receiver(post_delete, sender=Room)
def send_close_room_notification(sender, instance: Room, **kwargs):
    """Сигнал закрытия чата"""
    author = instance.author
    receiver = instance.receiver
    ChatNotification.objects.create(
        user=receiver, author=author, text=f"Chat with {author} is closed"
    )
    ChatNotification.objects.create(
        user=author, author=receiver, text=f"Chat with {receiver} is closed"
    )


@receiver(post_save, sender=Message)
def send_notification(sender, instance: Message, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        user_id = str(instance.author.id)
        # receiver_id = Room.objects.filter(id=instance.room.id).first().receiver.id

        data = {
            "message_id": instance.id,
            "read_status": instance.is_read,
            "chat_id": instance.room.id,
        }

        channel_name = f"message_{user_id}"
        async_to_sync(channel_layer.group_send)(
            channel_name, {"type": "send_message_status", "value": json.dumps(data)}
        )
