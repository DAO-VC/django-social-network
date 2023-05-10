from rest_framework import permissions

from profiles.models import Resume


class ResumePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Resume):
        if obj.professional_id.owner.id != request.user.id:
            return False
        return True
