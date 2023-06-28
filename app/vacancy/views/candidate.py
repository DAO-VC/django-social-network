from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from core.permissions import ProfessionalCreatePermission
from vacancy.models.candidate import Candidate
from vacancy.permissions import (
    ProfessionalMyApplicationsPermission,
    VacancyOwnerPermission,
    StartupCandidateFavoriteRetrievePermission,
    StartupCandidateFavoriteListPermission,
)
from vacancy.serializers.candidate import (
    CandidateCreateSerializer,
    CandidateBaseSerializer,
    StartupApproveCandidateSerializer,
    CandidateFavoriteSerializer,
)


class CandidateCreateView(generics.CreateAPIView):
    """Подача заявки на вступление в стартап для профессионала"""

    queryset = Candidate.objects.all()
    serializer_class = CandidateCreateSerializer
    permission_classes = (IsAuthenticated, ProfessionalCreatePermission)


class StartupRetrieveCandidates(generics.RetrieveDestroyAPIView):
    """Получение | удаление кандидата стартапа"""

    serializer_class = CandidateBaseSerializer
    permission_classes = (IsAuthenticated, StartupCandidateFavoriteRetrievePermission)

    def get_queryset(self):
        return Candidate.objects.select_related("professional_id", "vacancy_id").filter(
            Q(vacancy_id__company_id__owner=self.request.user)
            | Q(
                vacancy_id__company_id__work_team__candidate_id__professional_id__owner__in=[
                    self.request.user.id
                ]
            )
        )

    def perform_destroy(self, instance: Candidate):
        instance.accept_status = Candidate.AcceptStatus.DECLINE
        instance.save()
        return instance


class StartupApproveRetrieveCandidate(generics.UpdateAPIView):
    """Добавление кандидата в команду стартапа"""

    serializer_class = StartupApproveCandidateSerializer
    http_method_names = ["put"]
    permission_classes = (IsAuthenticated, StartupCandidateFavoriteRetrievePermission)

    def get_queryset(self):
        return Candidate.objects.select_related("professional_id", "vacancy_id").filter(
            Q(vacancy_id__company_id__owner=self.request.user)
            | Q(
                vacancy_id__company_id__work_team__candidate_id__professional_id__owner__in=[
                    self.request.user.id
                ]
            )
        )


class ListAllVacancyCandidates(generics.ListAPIView):
    """Получение списка всех кандидатов на вакансию стартапа"""

    serializer_class = CandidateBaseSerializer
    permission_classes = (IsAuthenticated, VacancyOwnerPermission)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["id", "base_status", "accept_status"]
    ordering_fields = ["base_status", "accept_status", "created_at"]

    def get_queryset(self):
        return Candidate.objects.select_related("professional_id", "vacancy_id").filter(
            vacancy_id=self.kwargs["pk"]
        )


class ProfessionalMyApplicationsListView(generics.ListAPIView):
    """Список всех заявок профессионала"""

    serializer_class = CandidateBaseSerializer
    permission_classes = (IsAuthenticated, ProfessionalMyApplicationsPermission)

    def get_queryset(self):
        return Candidate.objects.select_related("professional_id", "vacancy_id").filter(
            professional_id__owner_id=self.request.user.id
        )


class ProfessionalMyApplicationsRetrieveView(generics.RetrieveDestroyAPIView):
    """Получение | удаление заявки профессионала по id"""

    serializer_class = CandidateBaseSerializer
    http_method_names = ["get", "delete"]
    permission_classes = (IsAuthenticated, ProfessionalMyApplicationsPermission)

    def get_queryset(self):
        return Candidate.objects.select_related("professional_id", "vacancy_id").filter(
            professional_id__owner_id=self.request.user.id
        )


class CandidateFavoriteRetrieveView(generics.UpdateAPIView):
    """Добавление | удаление кандидата в фавориты"""

    serializer_class = CandidateFavoriteSerializer
    http_method_names = ["put"]
    permission_classes = (StartupCandidateFavoriteRetrievePermission,)

    def get_queryset(self):
        return Candidate.objects.select_related("professional_id", "vacancy_id").filter(
            Q(vacancy_id__company_id__owner=self.request.user)
            | Q(
                vacancy_id__company_id__work_team__candidate_id__professional_id__owner__in=[
                    self.request.user.id
                ]
            )
        )


class StartupFavoriteCandidates(generics.ListAPIView):
    """Список всех фаворитов кандидатов стартапа"""

    serializer_class = CandidateBaseSerializer
    permission_classes = (IsAuthenticated, StartupCandidateFavoriteListPermission)

    def get_queryset(self):
        return Candidate.objects.select_related("professional_id", "vacancy_id").filter(
            Q(vacancy_id__company_id__owner=self.request.user)
            | Q(
                vacancy_id__company_id__work_team__candidate_id__professional_id__owner__in=[
                    self.request.user.id
                ]
            ),
            is_favorite=True,
        )
