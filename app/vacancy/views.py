from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.permissions import (
    InvestorCreatePermission,
    StartupCreatePermission,
    UpdatePermission,
    ProfessionalCreatePermission,
)
from vacancy.filters import VacancyFilter
from vacancy.models import Vacancy, Offer, Candidate
from vacancy.permissions import OfferPermission
from vacancy.serializers import (
    VacancyCreateSerializer,
    VacancyUpdateSerializer,
    OfferCreateSerializer,
    OfferUpdateSerializer,
    VacancyBaseSerializer,
    CandidateCreateSerializer,
    CandidateBaseSerializer,
)


class VacancyListCreateView(generics.ListCreateAPIView):
    """Список всех вакансий стартапа | создание вакансии"""

    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer
    permission_classes = (IsAuthenticated, StartupCreatePermission)

    def get_queryset(self):
        return Vacancy.objects.filter(company_id__owner_id=self.request.user.id)


class VacancyRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение | удаление вакансии"""

    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer
    http_method_names = ["get", "put", "delete"]
    permission_classes = (IsAuthenticated, UpdatePermission)


class OfferListCreateView(generics.ListCreateAPIView):
    """Список всех оферов инвестора | создание офера"""

    queryset = Offer.objects.all()
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

    queryset = Candidate.objects.all()
    serializer_class = CandidateBaseSerializer

    def get_queryset(self):
        return Candidate.objects.filter(startup__owner=self.request.user)


class StartupRetrieveCandidates(generics.RetrieveDestroyAPIView):
    """Получение | удаление кандидата стартапа"""

    queryset = Candidate.objects.all()
    serializer_class = CandidateBaseSerializer

    def get_queryset(self):
        return Candidate.objects.filter(startup__owner=self.request.user)


class ProfessionalMyApplicationsListView(generics.ListAPIView):
    """Список всех заявок профессионала"""

    queryset = Candidate.objects.all()
    serializer_class = CandidateBaseSerializer

    def get_queryset(self):
        return Candidate.objects.filter(professional_id__owner_id=self.request.user.id)


class ProfessionalMyApplicationsRetrieveView(generics.RetrieveDestroyAPIView):
    """Получение | удаление заявки профессионала по id"""

    queryset = Candidate.objects.all()
    serializer_class = CandidateBaseSerializer
    http_method_names = ["get", "delete"]

    def get_queryset(self):
        return Candidate.objects.filter(professional_id__owner_id=self.request.user.id)
