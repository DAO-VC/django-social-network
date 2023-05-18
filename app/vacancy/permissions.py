from rest_framework import permissions

from vacancy.models import Offer, Vacancy


class OfferPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Offer):
        if obj.investor_id.owner.id != request.user.id:
            return False
        return True


class VacancyOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Vacancy):
        if obj.company_id.owner.id != request.user.id:
            return False
        return True
