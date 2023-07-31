from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from core.permissions import InvestorCreatePermission
from offer.filters import OfferModelFilter
from offer.models.offer import Offer
from offer.permissions import OfferVisiblePermission
from offer.serializers.offer import (
    OfferCreateSerializer,
    OfferUpdateSerializer,
    OfferBaseSerializer,
    OfferVisibleSerializer,
)


class OfferListCreateView(generics.ListCreateAPIView):
    """Список всех оферов инвестора | создание офера"""

    serializer_class = OfferCreateSerializer

    permission_classes = (IsAuthenticated, InvestorCreatePermission)

    def get_queryset(self):
        return Offer.objects.filter(investor_id__owner=self.request.user.id)


class OfferRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Получение | удаление | обновление офера"""

    serializer_class = OfferUpdateSerializer
    http_method_names = ["get", "put", "delete"]

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Offer.objects.filter(investor_id__owner=self.request.user.id)


class AllOffersList(generics.ListAPIView):
    """Список всех офферов платформы"""

    serializer_class = OfferBaseSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = OfferModelFilter
    ordering_fields = ["investor_id", "created_at"]
    search_fields = ("amount", "offer_information", "caption", "investor_id")

    def get_queryset(self):
        return Offer.objects.filter(is_visible=True)


class AllOffersRetrieve(generics.RetrieveAPIView):
    """Детальный вывод оффера платформы по id"""

    serializer_class = OfferBaseSerializer
    queryset = Offer.objects.all()
    permission_classes = (OfferVisiblePermission,)

    # def get_queryset(self):
    #     return Offer.objects.filter(is_visible=True)


class OfferVisibleRetrieveView(generics.UpdateAPIView):
    """Изменение видимости оффера"""

    queryset = Offer.objects.all()
    serializer_class = OfferVisibleSerializer
    http_method_names = ["put"]
    permission_classes = (OfferVisiblePermission,)


class InvestorAllOffers(generics.ListAPIView):
    """Список всех офферов инвестора по id"""

    serializer_class = OfferBaseSerializer

    # permission_classes = (IsAuthenticated, VacancyGetCreatePermission)

    def get_queryset(self):
        return Offer.objects.filter(investor_id=self.kwargs["pk"])
