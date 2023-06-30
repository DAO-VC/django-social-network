import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from chat.models import ChatNotification
from core.models import User
from vacancy.models.workteam import WorkTeam


@receiver(post_save, sender=WorkTeam)
def send_create_workteam_object(sender, instance: WorkTeam, created, **kwargs):
    if created:
        # channel_layer = get_channel_layer()
        receivers: list = [
            item.candidate_id.professional_id.owner.id
            for item in instance.startup_id.work_team.all()
        ]

        receivers.append(instance.startup_id.owner.id)
        # data = {
        #     'count': 1,
        #     'message': f"User '{instance.candidate_id.professional_id.owner}' has  to Workteam joined"
        # }
        # for receiver in receivers:
        #     channel_name = f'notify_{receiver}'
        #     async_to_sync(channel_layer.group_send)(
        #         channel_name, {
        #             'type': 'send_notification',
        #             'value': json.dumps(data)
        #         }
        #     )
        for receiver in receivers:
            user = User.objects.filter(id=receiver).first()
            ChatNotification.objects.create(
                user=user,
                text=f"User '{instance.candidate_id.professional_id.owner}' has  to Workteam joined",
            )


@receiver(post_delete, sender=WorkTeam)
def send_delete_workteam_object(sender, instance: WorkTeam, **kwargs):
    # channel_layer = get_channel_layer()
    receivers: list = [
        item.candidate_id.professional_id.owner.id
        for item in instance.startup_id.work_team.all()
    ]

    receivers.append(instance.startup_id.owner.id)
    # data = {
    #     'count': 1,
    #     'message': f"User '{instance.candidate_id.professional_id.owner}' has  to Workteam deleted"
    # }
    # for receiver in receivers:
    #     channel_name = f'notify_{receiver}'
    #     async_to_sync(channel_layer.group_send)(
    #         channel_name, {
    #             'type': 'send_notification',
    #             'value': json.dumps(data)
    #         }
    #     )
    user = User.objects.filter(id=receiver).first()
    ChatNotification.objects.create(
        user=user,
        text=f"User '{instance.candidate_id.professional_id.owner}' has  to Workteam deleted",
    )
