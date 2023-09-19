from django.db.models import Q

from core.admin import User
from chat.models import Room, Message


def banned_user_chats(status: str, author: User, receiver: User) -> None:
    if status == "banned":
        for room in Room.objects.filter(
            Q(author=author, receiver=receiver) | Q(author=receiver, receiver=author)
        ):
            room.status = Room.ChatStatus.BANNED
            room.save()

    else:
        for room in Room.objects.filter(
            Q(author=author, receiver=receiver) | Q(author=receiver, receiver=author)
        ):
            room.status = Room.ChatStatus.ACTIVE
            room.save()

        rooms_id = [
            room.id
            for room in Room.objects.filter(
                Q(author=author, receiver=receiver)
                | Q(author=receiver, receiver=author)
            )
        ]
        for id in rooms_id:

            banned_messages = Message.objects.filter(room_id=id, ban_status=True)

            for message in banned_messages:
                message.ban_status = False
                message.text = "System message : Chat unbanned."
                message.save()
