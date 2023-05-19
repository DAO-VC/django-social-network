from rest_framework import permissions

from profiles.models import Startup
from vacancy.models import Offer, Vacancy, Candidate


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


class WorkTeamOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Candidate):
        if obj.vacancy_id.company_id.owner.id != request.user.id:
            return False
        return True


class ListAllVacancyCandidatesPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Candidate):
        if obj.vacancy_id.company_id.owner.id != request.user.id:
            return False
        return True


class ProfessionalMyApplicationsPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Candidate):
        if obj.professional_id.owner.id != request.user.id:
            return False
        return True


class StartupCandidatesPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Candidate):
        if obj.vacancy_id.company_id.owner.id != request.user.id:
            return False
        return True
