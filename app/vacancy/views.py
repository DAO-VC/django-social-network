from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.permissions import (
    InvestorCreatePermission,
    StartupCreatePermission,
    UpdatePermission,
    ProfessionalCreatePermission,
)
from profiles.models import Startup
from vacancy.filters import VacancyFilter
from vacancy.models import Vacancy, Offer, Candidate
from vacancy.permissions import OfferPermission, VacancyOwnerPermission
from vacancy.serializers import (
    VacancyCreateSerializer,
    VacancyUpdateSerializer,
    OfferCreateSerializer,
    OfferUpdateSerializer,
    VacancyBaseSerializer,
    CandidateCreateSerializer,
    CandidateBaseSerializer,
    StartupApproveCandidateSerializer,
    VacancyVisibleSerializer,
)


class VacancyListCreateView(generics.ListCreateAPIView):
    """Список всех вакансий стартапа | создание вакансии"""

    serializer_class = VacancyCreateSerializer
    permission_classes = (IsAuthenticated, StartupCreatePermission)

    def get_queryset(self):
        return Vacancy.objects.filter(company_id__owner_id=self.request.user.id)


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


class OfferListCreateView(generics.ListCreateAPIView):
    """Список всех оферов инвестора | создание офера"""

    serializer_class = OfferCreateSerializer
    permission_classes = (IsAuthenticated, InvestorCreatePermission)

    def get_queryset(self):
        return Offer.objects.filter(investor_id__owner=self.request.user.id)


class OfferRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Получение | удаление | обновление офера"""

    queryset = Offer.objects.all()
    serializer_class = OfferUpdateSerializer
    http_method_names = ["get", "put", "delete"]
    permission_classes = [IsAuthenticated, OfferPermission]


class VacancyAllView(generics.ListAPIView):
    """Список всех вакансий | поиск по ним"""

    queryset = Vacancy.objects.all()
    serializer_class = VacancyBaseSerializer
    filterset_class = VacancyFilter
    permission_classes = (IsAuthenticated,)


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
    """Список всех кандидатов стартапа"""

    serializer_class = CandidateBaseSerializer

    def get_queryset(self):
        return Candidate.objects.filter(vacancy_id__company_id__owner=self.request.user)


class StartupRetrieveCandidates(generics.RetrieveDestroyAPIView):
    """Получение | удаление кандидата стартапа"""

    serializer_class = CandidateBaseSerializer

    def get_queryset(self):
        return Candidate.objects.filter(vacancy_id__company_id__owner=self.request.user)


class ProfessionalMyApplicationsListView(generics.ListAPIView):
    """Список всех заявок профессионала"""

    serializer_class = CandidateBaseSerializer

    def get_queryset(self):
        return Candidate.objects.filter(professional_id__owner_id=self.request.user.id)


class ProfessionalMyApplicationsRetrieveView(generics.RetrieveDestroyAPIView):
    """Получение | удаление заявки профессионала по id"""

    serializer_class = CandidateBaseSerializer
    http_method_names = ["get", "delete"]

    def get_queryset(self):
        return Candidate.objects.filter(professional_id__owner_id=self.request.user.id)


class StartupApproveRetrieveCandidate(generics.RetrieveUpdateAPIView):
    """Добавление кандидата в команду стартапа"""

    serializer_class = StartupApproveCandidateSerializer
    http_method_names = ["put"]

    def get_queryset(self):
        return Candidate.objects.filter(vacancy_id__company_id__owner=self.request.user)


class StartupWorkTeamList(generics.ListAPIView):
    """Список команды стартапа"""

    serializer_class = CandidateBaseSerializer

    def get_queryset(self):
        startup = Startup.objects.filter(owner__id=self.request.user.id).first()
        return startup.work_team.all()


class StartupWorkTeamRetrieveDelete(generics.RetrieveDestroyAPIView):
    """Удаление | получение члена команды"""

    serializer_class = CandidateBaseSerializer

    def get_queryset(self):
        startup = Startup.objects.filter(owner__id=self.request.user.id).first()
        return startup.work_team.all()
