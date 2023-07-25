from rest_framework import permissions

from offer.models.offer import Offer
from offer.models.offer_candidate import CandidateStartup


class OfferVisiblePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Offer):
        if obj.investor_id.owner.id == request.user.id:
            return True
        return False


class OfferStartupCandidatesPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: CandidateStartup):
        if obj.offer_id.investor_id.owner.id == request.user.id:
            return True
        return False


class StartupMyApplicationsPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: CandidateStartup):
        if obj.startup_id.owner.id != request.user.id:
            return False
        return True
