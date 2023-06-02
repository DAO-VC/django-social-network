from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.permissions import InvestorCreatePermission, UpdatePermission
from profiles.models.investor import Investor
from profiles.permissions import OnboardingPermission
from profiles.serializers.investor import (
    InvestorBaseSerializer,
    InvestorUpdateSerializer,
    InvestorSerializer,
)


class InvestorCreateView(generics.CreateAPIView):
    """Онбоардинг инвестор"""

    queryset = Investor.objects.all()
    serializer_class = InvestorBaseSerializer
    permission_classes = (
        IsAuthenticated,
        InvestorCreatePermission,
        OnboardingPermission,
    )


class InvestorUpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение инвестора"""

    serializer_class = InvestorUpdateSerializer
    http_method_names = [
        "get",
        "put",
    ]
    permission_classes = (IsAuthenticated, UpdatePermission)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return InvestorSerializer
        return InvestorUpdateSerializer

    def get_object(self):
        obj = Investor.objects.filter(owner__id=self.request.user.id).first()
        return obj


class AllInvestorsListView(generics.ListAPIView):
    """Список всех инвесторов сайта"""

    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer


class AllInvestorsRetrieveView(generics.RetrieveAPIView):
    """Детальное получение инвестора"""

    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer
