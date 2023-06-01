from rest_framework import permissions
from offer.models import Offer, CandidateStartup


class OfferVisiblePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Offer):
        if obj.investor_id.id == request.user.id:
            return True
        return False


class OfferStartupCandidates(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: CandidateStartup):
        if obj.offer_id.investor_id.id == request.user.id:
            return True
        return False
