from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.permissions import (
    InvestorCreatePermission,
    StartupCreatePermission,
    UpdatePermission,
)
from vacancy.filters import VacancyFilter
from vacancy.models import Vacancy, Offer
from vacancy.permissions import OfferPermission
from vacancy.serializers import (
    VacancyCreateSerializer,
    VacancyUpdateSerializer,
    OfferCreateSerializer,
    OfferUpdateSerializer,
    VacancyBaseSerializer,
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


class VacancyParamView(generics.ListAPIView):
    """Список всех вакансий | поиск по ним"""

    queryset = Vacancy.objects.all()
    serializer_class = VacancyBaseSerializer
    filterset_class = VacancyFilter
    permission_classes = (IsAuthenticated,)
