from rest_framework import permissions

from chat.models import Room


class RoomPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Room):
        if obj.author.id != request.user.id or obj.receiver.id != request.user.id:
            return False
        return True


class RoomOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Room):
        if obj.author.id != request.user.id:
            return False
        return True
