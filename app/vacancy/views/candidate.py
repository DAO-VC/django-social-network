from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from core.permissions import ProfessionalCreatePermission
from vacancy.models.candidate import Candidate
from vacancy.permissions import (
    StartupCandidatesPermission,
    ListAllVacancyCandidatesPermission,
    ProfessionalMyApplicationsPermission,
)
from vacancy.serializers.candidate import (
    CandidateCreateSerializer,
    CandidateBaseSerializer,
    StartupApproveCandidateSerializer,
    StartupAcceptRetrieveCandidate,
)


class CandidateCreateView(generics.CreateAPIView):
    """Подача заявки на вступление в стартап для профессионала"""

    queryset = Candidate.objects.all()
    serializer_class = CandidateCreateSerializer
    permission_classes = (IsAuthenticated, ProfessionalCreatePermission)


class StartupCandidates(generics.ListAPIView):
    """Список всех подтвержденных кандидатов стартапа"""

    serializer_class = CandidateBaseSerializer
    permission_classes = (IsAuthenticated, StartupCandidatesPermission)

    def get_queryset(self):
        return Candidate.objects.filter(
            vacancy_id__company_id__owner=self.request.user,
            accept_status=Candidate.AcceptStatus.ACCEPT,
        )


class StartupRetrieveCandidates(generics.RetrieveDestroyAPIView):
    """Получение | удаление кандидата стартапа"""

    serializer_class = CandidateBaseSerializer
    permission_classes = (IsAuthenticated, StartupCandidatesPermission)

    def get_queryset(self):
        return Candidate.objects.filter(vacancy_id__company_id__owner=self.request.user)


class StartupApproveRetrieveCandidate(generics.RetrieveUpdateAPIView):
    """Добавление кандидата в команду стартапа"""

    serializer_class = StartupApproveCandidateSerializer
    http_method_names = ["put"]
    permission_classes = (IsAuthenticated, ListAllVacancyCandidatesPermission)

    def get_queryset(self):
        return Candidate.objects.filter(vacancy_id__company_id__owner=self.request.user)


class StartupAcceptCandidate(generics.UpdateAPIView):
    """Добавление кандидата в список кандидатов стартапа"""

    serializer_class = StartupAcceptRetrieveCandidate
    http_method_names = ["put"]
    permission_classes = (IsAuthenticated, ListAllVacancyCandidatesPermission)

    def get_queryset(self):
        return Candidate.objects.filter(vacancy_id__company_id__owner=self.request.user)


class ListAllVacancyCandidates(generics.ListAPIView):
    """Получение списка всех кандидатов на вакансию стартапа"""

    serializer_class = CandidateBaseSerializer
    permission_classes = (IsAuthenticated, ListAllVacancyCandidatesPermission)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["id", "base_status", "accept_status"]
    ordering_fields = ["base_status", "accept_status", "created_at"]

    def get_queryset(self):
        return Candidate.objects.filter(vacancy_id=self.kwargs["pk"])


class ProfessionalMyApplicationsListView(generics.ListAPIView):
    """Список всех заявок профессионала"""

    serializer_class = CandidateBaseSerializer
    permission_classes = (IsAuthenticated, ProfessionalMyApplicationsPermission)

    def get_queryset(self):
        return Candidate.objects.filter(professional_id__owner_id=self.request.user.id)


class ProfessionalMyApplicationsRetrieveView(generics.RetrieveDestroyAPIView):
    """Получение | удаление заявки профессионала по id"""

    serializer_class = CandidateBaseSerializer
    http_method_names = ["get", "delete"]
    permission_classes = (IsAuthenticated, ProfessionalMyApplicationsPermission)

    def get_queryset(self):
        return Candidate.objects.filter(professional_id__owner_id=self.request.user.id)
