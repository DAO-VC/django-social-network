from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from chat.models import ChatNotification
from core.models import User
from offer.models.offer import ConfirmedOffer


@receiver(post_save, sender=ConfirmedOffer)
def send_create_investoffer_object(sender, instance: ConfirmedOffer, created, **kwargs):
    """Сигнал уведомления добавления нового офера"""
    if created:
        receiver: User = instance.startup_id.owner

        ChatNotification.objects.create(
            user=receiver,
            text=f"Now you are  invested by  investor '{instance.investor_id.name}'.",
        )


@receiver(post_delete, sender=ConfirmedOffer)
def send_delete_investoffer_object(sender, instance: ConfirmedOffer, **kwargs):
    """Сигнал уведомления удаления подтвержденного офера"""

    receiver: User = instance.startup_id.owner

    ChatNotification.objects.create(
        user=receiver,
        text=f"You are no longer invested by '{instance.investor_id.name}'.",
    )
