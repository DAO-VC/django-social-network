from django.db import models
from django_extensions.db.fields import CreationDateTimeField

from core.models import User


class Room(models.Model):
    """Сущность/модель чат"""

    author = models.ForeignKey(
        User, related_name="author_room", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name="receiver_room", on_delete=models.CASCADE
    )
    created_at = CreationDateTimeField(
        verbose_name="Дата создания",
    )


class Message(models.Model):
    """Модель сообщения чата"""

    author = models.ForeignKey(
        User, related_name="author_messages", on_delete=models.CASCADE
    )
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE)
    text = models.CharField(max_length=200, blank=True, null=True)
    created_at = CreationDateTimeField(
        verbose_name="Дата создания",
    )

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.text + " " + str(self.created_at)


class ChatNotification(models.Model):
    """Базовая модель уведомлений приложения"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reciever")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author", null=True
    )
    text = models.TextField(null=True)
    is_seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username
