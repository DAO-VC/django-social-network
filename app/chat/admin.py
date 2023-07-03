from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from chat.models import Message, Room, ChatNotification


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "author_link", "receiver_link", "created_at")

    list_filter = (
        ("author", admin.RelatedOnlyFieldListFilter),
        ("receiver", admin.RelatedOnlyFieldListFilter),
    )
    ordering = ("created_at",)

    def author_link(self, room: Room):
        url = reverse("admin:core_user_change", args=[room.author.id])
        link = '<a href="%s">%s</a>' % (url, room.author.id)
        return mark_safe(link)

    author_link.short_description = "Автор чата"

    def receiver_link(self, room: Room):
        url = reverse("admin:core_user_change", args=[room.receiver.id])
        link = '<a href="%s">%s</a>' % (url, room.receiver.id)
        return mark_safe(link)

    receiver_link.short_description = "Участник чата"


@admin.register(Message)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "author_link", "room_link", "created_at")

    list_filter = (
        ("author", admin.RelatedOnlyFieldListFilter),
        ("room", admin.RelatedOnlyFieldListFilter),
    )
    ordering = ("created_at",)

    def author_link(self, message: Message):
        url = reverse("admin:core_user_change", args=[message.author.id])
        link = '<a href="%s">%s</a>' % (url, message.author.id)
        return mark_safe(link)

    author_link.short_description = "Автор сообщения"

    def room_link(self, message: Message):
        url = reverse("admin:chat_room_change", args=[message.room.id])
        link = '<a href="%s">%s</a>' % (url, message.room.id)
        return mark_safe(link)

    room_link.short_description = "Чат/комната"


@admin.register(ChatNotification)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("id", "receiver_link", "is_seen")

    list_filter = (
        ("user", admin.RelatedOnlyFieldListFilter),
        ("author", admin.RelatedOnlyFieldListFilter),
        "is_seen",
    )
    ordering = ("is_seen",)

    def author_link(self, notification: ChatNotification):
        url = reverse("admin:core_user_change", args=[notification.author.id])
        link = '<a href="%s">%s</a>' % (url, notification.author.id)
        return mark_safe(link)

    author_link.short_description = "Автор уведомления(опционально)"

    def receiver_link(self, notification: ChatNotification):
        url = reverse("admin:core_user_change", args=[notification.user.id])
        link = '<a href="%s">%s</a>' % (url, notification.user.id)
        return mark_safe(link)

    receiver_link.short_description = "Получатель уведомления"
