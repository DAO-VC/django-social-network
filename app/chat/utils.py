from django.db.models import Q

from core.admin import User
from chat.models import Room


def banned_user_chats(status: str, author: User, receiver: User) -> None:
    if status == "banned":
        for room in Room.objects.filter(author=author, receiver=receiver) | Q(
            author=receiver, receiver=author
        ):
            room.status = Room.ChatStatus.BANNED
            room.save()

    else:
        for room in Room.objects.filter(author=author, receiver=receiver) | Q(
            author=receiver, receiver=author
        ):
            room.status = Room.ChatStatus.ACTIVE
            room.save()
