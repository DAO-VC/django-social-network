from rest_framework import generics
from vacancy.models import Vacancy, Offer
from vacancy.permissions import OfferPermission
from vacancy.serializers import (
    VacancyCreateSerializer,
    VacancyUpdateSerializer,
    OfferCreateSerializer,
    OfferUpdateSerializer,
)


class VacancyListCreateView(generics.ListCreateAPIView):
    """Список всех вакансий стартапа | создание вакансии"""

    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer

    def get_queryset(self):
        return Vacancy.objects.filter(company_id__owner_id=self.request.user.id)


class VacancyRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение | удаление вакансии"""

    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer
    http_method_names = ["get", "put", "delete"]


class OfferListCreateView(generics.ListCreateAPIView):
    """Список всех оферов инвестора | создание офера"""

    queryset = Offer.objects.all()
    serializer_class = OfferCreateSerializer

    def get_queryset(self):
        return Offer.objects.filter(investor_id__owner=self.request.user.id)


class OfferRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Получение | удаление | обновление офера"""

    queryset = Offer.objects.all()
    serializer_class = OfferUpdateSerializer
    http_method_names = ["get", "put", "delete"]
    permission_classes = [OfferPermission]
