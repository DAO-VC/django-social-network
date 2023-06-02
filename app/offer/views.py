from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from core.permissions import StartupCreatePermission, InvestorCreatePermission
from offer.models import Offer, CandidateStartup, ConfirmedOffer
from offer.permissions import OfferVisiblePermission, OfferStartupCandidatesPermission
from offer.serializers import (
    OfferUpdateSerializer,
    OfferCreateSerializer,
    OfferBaseSerializer,
    OfferVisibleSerializer,
    ConfirmOfferSerializer,
    CandidateStartupCreateSerializer,
    CandidateStartupBaseSerializer,
    ConfirmedOfferInvestorSerializer,
    ConfirmedOfferStartupSerializer,
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

    def get_queryset(self):
        return Offer.objects.filter(is_visible=True)


class AllOffersRetrieve(generics.RetrieveAPIView):
    """Детальный вывод оффера платформы по id"""

    serializer_class = OfferBaseSerializer

    def get_queryset(self):
        return Offer.objects.filter(is_visible=True)


class OfferVisibleRetrieveView(generics.UpdateAPIView):
    """Изменение видимости оффера"""

    queryset = Offer.objects.all()
    serializer_class = OfferVisibleSerializer
    http_method_names = ["put"]
    permission_classes = (OfferVisiblePermission,)


class StartupCandidateCreateView(generics.CreateAPIView):
    """Подача заявки на оффер стартапом"""

    queryset = CandidateStartup
    serializer_class = CandidateStartupCreateSerializer
    permission_classes = (IsAuthenticated, StartupCreatePermission)


class ListAllOfferCandidates(generics.ListAPIView):
    """Получение списка всех кандидатов на оффер инвестора"""

    serializer_class = CandidateStartupBaseSerializer
    # permission_classes = (IsAuthenticated, ListAllVacancyCandidatesPermission)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["id", "accept_status"]
    ordering_fields = ["accept_status", "created_at"]

    def get_queryset(self):
        return CandidateStartup.objects.filter(offer_id=self.kwargs["pk"])


class OfferStartupCandidates(generics.ListAPIView):
    """Список всех кандидатов инвестора"""

    serializer_class = CandidateStartupBaseSerializer

    permission_classes = (OfferStartupCandidatesPermission,)

    def get_queryset(self):
        return CandidateStartup.objects.filter(
            offer_id__investor_id__owner=self.request.user
        )


class OfferRetrieveStartupCandidates(generics.RetrieveDestroyAPIView):
    """Получение | удаление кандидата на оффер"""

    serializer_class = CandidateStartupBaseSerializer

    permission_classes = (OfferStartupCandidatesPermission,)

    def get_queryset(self):
        return CandidateStartup.objects.filter(
            offer_id__investor_id__owner=self.request.user
        )


class ConfirmOfferView(generics.UpdateAPIView):
    """Изменение статуса стартап-кандидата на ACCEPT"""

    serializer_class = ConfirmOfferSerializer
    http_method_names = ["put"]
    permission_classes = (OfferStartupCandidatesPermission,)

    def get_queryset(self):
        return CandidateStartup.objects.filter(
            offer_id__investor_id__owner=self.request.user
        )


class InvestorConfirmedStartupsList(generics.ListAPIView):
    """Список всех инвестируемых проектов инвестора"""

    serializer_class = ConfirmedOfferInvestorSerializer
    permission_classes = (OfferStartupCandidatesPermission,)

    def get_queryset(self):
        return ConfirmedOffer.objects.filter(
            investor_id__owner=self.request.user,
        )


class StartupConfirmedList(generics.ListAPIView):
    """Список всех инвесторов стартапа"""

    serializer_class = ConfirmedOfferStartupSerializer
    permission_classes = (IsAuthenticated, StartupCreatePermission)

    def get_queryset(self):
        return ConfirmedOffer.objects.filter(
            startup_id__owner=self.request.user,
        )


class StartupConfirmedRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    """Детальный просмотр | удаление подтвержденного стартапа"""

    serializer_class = ConfirmedOfferInvestorSerializer

    def get_queryset(self):
        return ConfirmedOffer.objects.filter(
            investor_id__owner=self.request.user,
        )


class InvestorAllOffers(generics.ListAPIView):
    """Список всех офферов инвестора по id"""

    serializer_class = OfferBaseSerializer

    # permission_classes = (IsAuthenticated, VacancyGetCreatePermission)

    def get_queryset(self):
        return Offer.objects.filter(investor_id=self.kwargs["pk"])
