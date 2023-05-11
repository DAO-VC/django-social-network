from rest_framework import permissions

from profiles.models import Startup


class StartupCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.profile != "startup":
            return False
        return True


class UpdatePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Startup):
        if obj.owner.id != request.user.id:
            return False
        return True


class ProfessionalCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.profile != "professional":
            return False


class InvestorCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.profile != "investor":
            return False
        return True
