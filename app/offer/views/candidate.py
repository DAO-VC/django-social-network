from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from core.permissions import StartupCreatePermission
from offer.models.offer import ConfirmedOffer
from offer.models.offer_candidate import CandidateStartup
from offer.permissions import (
    OfferStartupCandidatesPermission,
    StartupMyApplicationsPermission,
)
from offer.serializers.candidate import (
    CandidateStartupCreateSerializer,
    CandidateStartupBaseSerializer,
    InvestCandidateFavoriteSerializer,
)
from offer.serializers.offer import (
    ConfirmOfferSerializer,
    ConfirmedOfferInvestorSerializer,
)


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
    search_fields = ("about", "startup_id__name")

    def get_queryset(self):
        return CandidateStartup.objects.filter(
            offer_id=self.kwargs["pk"],
            accept_status=CandidateStartup.AcceptStatus.PENDING_FOR_APPROVAL,
        )


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

    def perform_destroy(self, instance: CandidateStartup):
        instance.accept_status = CandidateStartup.AcceptStatus.DECLINE
        instance.save()
        return instance


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

    # serializer_class = ConfirmedOfferInvestorSerializer
    # permission_classes = (OfferStartupCandidatesPermission,)
    #
    # def get_queryset(self):
    #     return ConfirmedOffer.objects.filter(
    #         investor_id__owner=self.request.user,
    #     )
    serializer_class = CandidateStartupBaseSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return CandidateStartup.objects.filter(
            offer_id__investor_id__owner=self.request.user,
            accept_status=CandidateStartup.AcceptStatus.ACCEPT,
        )


class StartupConfirmedList(generics.ListAPIView):
    """Список всех инвесторов стартапа"""

    serializer_class = CandidateStartupBaseSerializer
    permission_classes = (IsAuthenticated, StartupCreatePermission)

    def get_queryset(self):
        return CandidateStartup.objects.filter(
            startup_id__owner=self.request.user,
            accept_status=CandidateStartup.AcceptStatus.ACCEPT,
        )


class StartupConfirmedRetrieveDeleteView(generics.RetrieveDestroyAPIView):
    """Детальный просмотр | удаление подтвержденного стартапа"""

    serializer_class = ConfirmedOfferInvestorSerializer

    def get_queryset(self):
        return ConfirmedOffer.objects.filter(
            investor_id__owner=self.request.user,
        )

    def perform_destroy(self, instance: ConfirmedOffer):
        candidate = CandidateStartup.objects.filter(
            startup_id=instance.startup_id.id, offer_id=instance.offer_id.id
        ).first()
        candidate.accept_status = CandidateStartup.AcceptStatus.CONCLUDED
        candidate.save()
        super().perform_destroy(instance)


class StartupMyApplications(generics.ListAPIView):
    """Список всех заявок стартапа на инвестиции"""

    serializer_class = CandidateStartupBaseSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return CandidateStartup.objects.filter(
            startup_id__owner=self.request.user,
        )


class StartupMyApplicationsRetrieveView(generics.RetrieveDestroyAPIView):
    """Получение | удаление заявки стартапа по id"""

    serializer_class = CandidateStartupBaseSerializer
    http_method_names = ["get", "delete"]
    permission_classes = (IsAuthenticated, StartupMyApplicationsPermission)

    def get_queryset(self):
        return CandidateStartup.objects.filter(
            startup_id__owner=self.request.user,
        )


class OfferFavoriteCandidates(generics.ListAPIView):
    """Список всех фаворитов кандидатов инвестора"""

    serializer_class = CandidateStartupBaseSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return CandidateStartup.objects.filter(
            offer_id__investor_id__owner=self.request.user, is_favorite=True
        )


class InvestCandidateFavoriteRetrieveView(generics.UpdateAPIView):
    """Добавление | удаление кандидата в фавориты"""

    serializer_class = InvestCandidateFavoriteSerializer
    http_method_names = ["put"]
    permission_classes = (OfferStartupCandidatesPermission,)
    queryset = CandidateStartup.objects.all()
