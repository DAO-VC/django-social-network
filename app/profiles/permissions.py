from rest_framework import permissions

from profiles.models.startup import Startup
from vacancy.models.workteam import WorkTeam


class OnboardingPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_onboarding:
            return False
        return True


class UpdateStartupPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Startup):
        if request.method == "PUT":
            if obj.owner.id == request.user.id:
                return True
            if request.user.id in [
                item.candidate_id.professional_id.owner.id
                for item in obj.work_team.all()
            ]:
                work_obj: WorkTeam = obj.work_team.filter(
                    candidate_id__professional_id__owner_id=request.user.id
                ).first()
                if work_obj.company_management:
                    return True
        if request.method == "GET":
            return True
        return False
