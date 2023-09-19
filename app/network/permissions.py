from rest_framework import permissions

from network.models import Network


class NetworkOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Network):
        if request.user == obj.owner:
            return True
        return False
