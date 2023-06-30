import json

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.signals import post_save
from core.models import User
from django.dispatch import receiver


@receiver(post_save, sender=User)
def send_OnlineStatus(sender, instance: User, created, **kwargs):
    if not created:
        channel_layer = get_channel_layer()
        email = instance.email
        user_status = instance.online

        data = {"email": email, "status": user_status}
        async_to_sync(channel_layer.group_send)(
            "user", {"type": "send_OnlineStatus", "value": json.dumps(data)}
        )
