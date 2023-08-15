from django.db import models
from django_extensions.db.fields import CreationDateTimeField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from core.models import User


class Room(models.Model):
    """Сущность/модель чат"""

    author = models.ForeignKey(
        User, related_name="author_room", on_delete=models.CASCADE, verbose_name="Автор"
    )
    receiver = models.ForeignKey(
        User,
        related_name="receiver_room",
        on_delete=models.CASCADE,
        verbose_name="Участник чата",
    )
    created_at = CreationDateTimeField(
        verbose_name="Дата создания",
    )
    limit = models.Q(app_label="vacancy", model="candidate") | models.Q(
        app_label="offer", model="candidateStartup"
    )
    content_type = models.ForeignKey(
        ContentType,
        blank=True,
        null=True,
        limit_choices_to=limit,
        related_name="content_type",
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = "Чат/Комната"
        verbose_name_plural = "Чаты/Комнаты"

    def __str__(self):
        return f"{self.id} - Чат"


class Message(models.Model):
    """Модель сообщения чата"""

    author = models.ForeignKey(
        User,
        related_name="author_messages",
        on_delete=models.CASCADE,
        verbose_name="Автор",
    )
    room = models.ForeignKey(
        Room,
        related_name="messages",
        on_delete=models.CASCADE,
        verbose_name="Чат/комната",
    )
    text = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Текст сообщения"
    )
    created_at = CreationDateTimeField(
        verbose_name="Дата создания",
    )
    is_read = models.BooleanField(verbose_name="Прочитано", null=True, blank=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.text + " " + str(self.created_at)


class ChatNotification(models.Model):
    """Базовая модель уведомлений приложения"""

    user = models.ForeignKey(
        User,
        # on_delete=models.SET_NULL,
        on_delete=models.CASCADE,
        related_name="reciever",
        verbose_name="Получатель уведомления",
        null=True,
    )
    author = models.ForeignKey(
        User,
        # on_delete=models.SET_NULL,
        on_delete=models.CASCADE,
        related_name="author",
        null=True,
        verbose_name="Автор(опционально)",
    )
    text = models.TextField(null=True, verbose_name="Текст уведомления")
    is_seen = models.BooleanField(default=False, verbose_name="Просмотрено")

    class Meta:
        verbose_name = "Уведомление"
        verbose_name_plural = "Уведомления"

    def __str__(self) -> str:
        return self.user.username
