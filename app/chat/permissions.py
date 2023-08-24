from rest_framework import permissions

from chat.models import Room


class RoomPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Room):
        if obj.author.id != request.user.id or obj.receiver.id != request.user.id:
            return True
        return False


class RoomOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Room):
        if obj.author.id != request.user.id:
            return True
        return False


class RoomPermissionNotObj(permissions.BasePermission):
    def has_permission(self, request, view):
        room = Room.objects.filter(id=view.kwargs["pk"]).first()
        if room.author.id != request.user.id or room.receiver.id != request.user.id:
            return True
        return False
