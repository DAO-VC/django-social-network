from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from core.permissions import (
    ProfessionalCreatePermission,
)
from profiles.models import Startup
from profiles.serializers import StartupSerializer
from vacancy.models import Vacancy, Candidate
from vacancy.permissions import (
    VacancyOwnerPermission,
    ListAllVacancyCandidatesPermission,
    ProfessionalMyApplicationsPermission,
    StartupCandidatesPermission,
    StartupWorkTeamPermission,
    StartupWorkTeamUpdatePermission,
    VacancyGetCreatePermission,
)
from vacancy.serializers import (
    VacancyCreateSerializer,
    VacancyUpdateSerializer,
    VacancyBaseSerializer,
    CandidateCreateSerializer,
    CandidateBaseSerializer,
    StartupApproveCandidateSerializer,
    VacancyVisibleSerializer,
    StartupAcceptRetrieveCandidate,
    WorkTeamBaseSerializer,
    WorkTeamUpdatePermissionsSerializer,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class VacancyListCreateView(generics.ListCreateAPIView):
    """Список всех вакансий стартапа | создание вакансии"""

    serializer_class = VacancyCreateSerializer
    permission_classes = (IsAuthenticated, VacancyGetCreatePermission)

    def get_queryset(self):
        return Vacancy.objects.filter(
            Q(
                company_id__work_team__candidate_id__professional_id__owner__in=[
                    self.request.user.id
                ]
            )
            | Q(company_id__owner=self.request.user.id)
        )


class VacancyRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение | удаление вакансии"""

    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer
    http_method_names = ["get", "put", "delete"]
    permission_classes = (IsAuthenticated, VacancyOwnerPermission)


class VacancyVisibleRetrieveView(generics.UpdateAPIView):
    """Изменение видимости вакансии"""

    queryset = Vacancy.objects.all()
    serializer_class = VacancyVisibleSerializer
    http_method_names = ["put"]
    permission_classes = (IsAuthenticated, VacancyOwnerPermission)


class VacancyAllView(generics.ListAPIView):
    """Список всех вакансий | поиск по ним"""

    serializer_class = VacancyBaseSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["id", "company_id", "salary", "requirements"]
    ordering_fields = ["company_id", "position", "salary", "requirements", "created_at"]

    def get_queryset(self):
        return Vacancy.objects.filter(is_visible=True)


class VacancyAllDetailView(generics.RetrieveAPIView):
    """Все вакансии по id"""

    queryset = Vacancy.objects.all()
    serializer_class = VacancyBaseSerializer
    http_method_names = ["get"]


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


class ProfessionalWorkView(generics.ListAPIView):
    """Отображение рабочего стартапа профессионала"""

    serializer_class = StartupSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Startup.objects.filter(
            work_team__candidate_id__professional_id__owner=self.request.user.id
        )


class StartupAllVacancies(generics.ListAPIView):
    """Список всех вакансий стартапа по id"""

    serializer_class = VacancyBaseSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Vacancy.objects.filter(company_id=self.kwargs["pk"])
