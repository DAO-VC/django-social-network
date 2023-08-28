from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from core.permissions import InvestorCreatePermission
from offer.filters import OfferModelFilter
from offer.models.offer import Offer
from offer.models.offer_candidate import CandidateStartup
from offer.permissions import OfferVisiblePermission
from offer.serializers.offer import (
    OfferCreateSerializer,
    OfferUpdateSerializer,
    OfferBaseSerializer,
    OfferVisibleSerializer,
)


class OfferListCreateView(generics.ListCreateAPIView):
    """Список всех оферов инвестора | создание офера"""

    permission_classes = (IsAuthenticated, InvestorCreatePermission)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    ordering_fields = ["created_at"]
    filterset_fields = ["id", "active_status"]

    def get_queryset(self):
        return Offer.objects.filter(investor_id__owner=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OfferCreateSerializer
        return OfferBaseSerializer


class OfferRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Получение | удаление | обновление офера"""

    serializer_class = OfferUpdateSerializer
    http_method_names = ["get", "put", "delete"]

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Offer.objects.filter(investor_id__owner=self.request.user.id)

    def perform_destroy(self, instance: Offer):
        instance.active_status = Offer.ActiveStatus.ARCHIVE
        instance.save()
        candidates = CandidateStartup.objects.filter(offer_id=instance.id)
        for candidate in candidates:
            if candidate.accept_status != CandidateStartup.AcceptStatus.ACCEPT:
                candidate.accept_status = (
                    CandidateStartup.AcceptStatus.THE_OFFER_IS_OUT_OF_ORDER
                )
                candidate.save()
        return instance


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
        return Offer.objects.filter(is_visible=True, active_status=True)


class AllOffersRetrieve(generics.RetrieveAPIView):
    """Детальный вывод оффера платформы по id"""

    serializer_class = OfferBaseSerializer
    queryset = Offer.objects.all()
    # permission_classes = (OfferVisiblePermission,)

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
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    ordering_fields = ["created_at"]

    # permission_classes = (IsAuthenticated, VacancyGetCreatePermission)

    def get_queryset(self):
        return Offer.objects.filter(investor_id=self.kwargs["pk"])
