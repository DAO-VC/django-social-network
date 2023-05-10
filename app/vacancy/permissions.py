from rest_framework import permissions

from vacancy.models import Offer


class OfferPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Offer):
        if obj.investor_id.owner.id != request.user.id:
            return False
        return True
