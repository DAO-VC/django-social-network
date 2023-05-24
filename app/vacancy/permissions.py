from django.db.models import Q
from rest_framework import permissions
from rest_framework.exceptions import NotFound

from profiles.models import Startup
from vacancy.models import Offer, Vacancy, Candidate, WorkTeam


class OfferPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Offer):
        if obj.investor_id.owner.id != request.user.id:
            return False
        return True


class VacancyOwnerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        obj = Vacancy.objects.filter(id=view.kwargs["pk"]).first()
        try:
            startup: Startup = Startup.objects.get(owner=obj.company_id.owner)
        except AttributeError:
            raise NotFound("Object don't exist")

        if obj.company_id.owner.id == request.user.id:
            return True
        if request.user.id in [
            item.candidate_id.professional_id.owner.id
            for item in startup.work_team.all()
        ]:
            work_obj: WorkTeam = startup.work_team.filter(
                candidate_id__professional_id__owner_id=request.user.id
            ).first()
            if work_obj.vacancy_management:
                return True
        return False


class WorkTeamOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: WorkTeam):
        if obj.candidate_id.vacancy_id.company_id.owner.id != request.user.id:
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


class StartupWorkTeamPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Startup):
        if not obj:
            raise NotFound("Object don't exist")
        if obj.owner.id == request.user.id:
            return True
        if request.user.id in [
            item.candidate_id.professional_id.owner.id for item in obj.work_team.all()
        ]:
            return True
        return False


class StartupWorkTeamUpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        startup = Startup.objects.filter(
            Q(work_team__candidate_id__professional_id__owner__in=[request.user.id])
            | Q(owner=request.user.id)
        ).first()
        if not startup:
            raise NotFound("Object don't exist")
        if startup.owner.id == request.user.id:
            return True
        if request.user.id in [
            item.candidate_id.professional_id.owner.id
            for item in startup.work_team.all()
        ]:
            work_obj: WorkTeam = startup.work_team.filter(
                candidate_id__professional_id__owner_id=request.user.id
            ).first()
            if work_obj.performers_management:
                return True
        return False


class VacancyGetCreatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        startup = Startup.objects.filter(
            Q(work_team__candidate_id__professional_id__owner__in=[request.user.id])
            | Q(owner=request.user.id)
        ).first()

        if not startup:
            raise NotFound("Object don't exist")
        if request.method == "GET":
            return True

        if request.method == "POST":
            if startup.owner.id == request.user.id:
                return True
            if request.user.id in [
                item.candidate_id.professional_id.owner.id
                for item in startup.work_team.all()
            ]:
                work_obj: WorkTeam = startup.work_team.filter(
                    candidate_id__professional_id__owner_id=request.user.id
                ).first()
                if work_obj.vacancy_management:
                    return True
            return False
