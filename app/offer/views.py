from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from offer.models import Offer
from offer.serializers import (
    OfferUpdateSerializer,
    OfferCreateSerializer,
    OfferBaseSerializer,
    OfferVisibleSerializer,
)


class OfferListCreateView(generics.ListCreateAPIView):
    """Список всех оферов инвестора | создание офера"""

    serializer_class = OfferCreateSerializer

    # permission_classes = (IsAuthenticated, InvestorCreatePermission)

    def get_queryset(self):
        return Offer.objects.filter(investor_id__owner=self.request.user.id)


class OfferRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Получение | удаление | обновление офера"""

    queryset = Offer.objects.all()
    serializer_class = OfferUpdateSerializer
    http_method_names = ["get", "put", "delete"]
    # permission_classes = [IsAuthenticated, OfferPermission]


class AllOffersList(generics.ListAPIView):
    """Список всех офферов платформы"""

    serializer_class = OfferBaseSerializer

    def get_queryset(self):
        return Offer.objects.filter(is_visible=True)


class AllOffersRetrieve(generics.RetrieveAPIView):
    """Детальный вывод ооффера платформы по id"""

    serializer_class = OfferBaseSerializer

    def get_queryset(self):
        return Offer.objects.filter(is_visible=True)


class OfferVisibleRetrieveView(generics.UpdateAPIView):
    """Изменение видимости оффера"""

    queryset = Offer.objects.all()
    serializer_class = OfferVisibleSerializer
    http_method_names = ["put"]
