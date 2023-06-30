from django.contrib import admin

from chat.models import Message, Room, ChatNotification

# Register your models here.

admin.site.register(Room)
admin.site.register(Message)
admin.site.register(ChatNotification)
