from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from profiles.models.startup import Startup
from vacancy.models.candidate import Candidate
from vacancy.models.workteam import WorkTeam
from vacancy.permissions import (
    StartupWorkTeamPermission,
    StartupWorkTeamUpdatePermission,
    ProfessionalMyApplicationsPermission,
)
from vacancy.serializers.candidate import CandidateBaseSerializer
from vacancy.serializers.workteam import (
    WorkTeamBaseSerializer,
    WorkTeamUpdatePermissionsSerializer,
)


class StartupWorkTeamList(generics.ListAPIView):
    """Список команды стартапа"""

    serializer_class = WorkTeamBaseSerializer
    permission_classes = (IsAuthenticated, StartupWorkTeamPermission)

    def get_queryset(self):
        obj = Startup.objects.filter(
            Q(
                work_team__candidate_id__professional_id__owner__in=[
                    self.request.user.id
                ]
            )
            | Q(owner=self.request.user.id)
        ).first()
        self.check_object_permissions(self.request, obj)
        return obj.work_team.all()


class StartupWorkTeamRetrieveDelete(generics.RetrieveUpdateDestroyAPIView):
    """Удаление | изменение | получение члена команды"""

    permission_classes = (IsAuthenticated, StartupWorkTeamUpdatePermission)
    http_method_names = ["get", "put", "delete"]

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return WorkTeamUpdatePermissionsSerializer
        return WorkTeamBaseSerializer

    def get_queryset(self):
        obj = Startup.objects.filter(
            Q(
                work_team__candidate_id__professional_id__owner__in=[
                    self.request.user.id
                ]
            )
            | Q(owner=self.request.user.id)
        ).first()
        self.check_object_permissions(self.request, obj)
        return obj.work_team.all()

    def perform_destroy(self, instance: WorkTeam):
        candidate = Candidate.objects.filter(id=instance.candidate_id.id).first()
        candidate.accept_status = Candidate.AcceptStatus.CONCLUDED
        candidate.save()
        super().perform_destroy(instance)


# class ProfessionalWorkView(generics.ListAPIView):
#     """Отображение рабочего стартапа профессионала"""
#
#     serializer_class = StartupSerializer
#     permission_classes = (IsAuthenticated,)
#
#     def get_queryset(self):
#         return Startup.objects.filter(
#             work_team__candidate_id__professional_id__owner=self.request.user.id
#         )


class ProfessionalWorkView(generics.ListAPIView):
    """Отображение работы профессионала"""

    serializer_class = CandidateBaseSerializer
    permission_classes = (IsAuthenticated, ProfessionalMyApplicationsPermission)

    def get_queryset(self):
        return Candidate.objects.select_related("professional_id", "vacancy_id").filter(
            professional_id__owner_id=self.request.user.id,
            accept_status=Candidate.AcceptStatus.IN_THE_TEAM,
        )
