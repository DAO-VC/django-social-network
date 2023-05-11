from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from core.permissions import (
    StartupCreatePermission,
    ProfessionalCreatePermission,
    InvestorCreatePermission,
    UpdatePermission,
)
from profiles.models import (
    Startup,
    Professional,
    Investor,
    Industries,
    SaleRegions,
    BusinessType,
)

from profiles.serializers import (
    StartupBaseSerializer,
    ProfessionalBaseSerializer,
    InvestorBaseSerializer,
    StartupUpdateSerializer,
    ProfessionalUpdateSerializer,
    InvestorUpdateSerializer,
    IndustriesSerializer,
    SaleRegionSerializer,
    BusinessTypeSerializer,
    StartupSerializer,
    ProfessionalSerializer,
    InvestorSerializer,
)


class StartUpCreateView(generics.CreateAPIView):
    """Онбоардинг стартап"""

    queryset = Startup.objects.all()
    serializer_class = StartupBaseSerializer
    permission_classes = (IsAuthenticated, StartupCreatePermission)

    # def get_queryset(self):
    #     return Startup.objects.filter(owner__id=self.request.user.id)


class ProfessionalCreateView(generics.CreateAPIView):
    """Онбоардинг профессионал"""

    queryset = Professional.objects.all()
    serializer_class = ProfessionalBaseSerializer
    permission_classes = (IsAuthenticated, ProfessionalCreatePermission)

    # def get_queryset(self):
    #     return Professional.objects.filter(owner__id=self.request.user.id)


class InvestorCreateView(generics.CreateAPIView):
    """Онбоардинг инвестор"""

    queryset = Investor.objects.all()
    serializer_class = InvestorBaseSerializer
    permission_classes = (IsAuthenticated, InvestorCreatePermission)

    # def get_queryset(self):
    #     return Investor.objects.filter(owner__id=self.request.user.id)


# class StartListCreateView(generics.ListCreateAPIView):
#     """Создание стартапа"""
#     queryset = Startup.objects.all()
#     serializer_class = StartupBaseSerializer


class StartUpUpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение стартапа"""

    queryset = Startup.objects.all()
    serializer_class = StartupUpdateSerializer
    http_method_names = ["get", "put"]
    permission_classes = (IsAuthenticated, UpdatePermission)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return StartupSerializer
        return StartupUpdateSerializer

    def get_object(self):
        obj = Startup.objects.filter(owner__id=self.request.user.id).first()
        return obj


class ProfessionalUpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение профессионала"""

    serializer_class = ProfessionalUpdateSerializer
    http_method_names = [
        "get",
        "put",
    ]
    permission_classes = (IsAuthenticated, UpdatePermission)

    def get_object(self):
        obj = Professional.objects.filter(owner__id=self.request.user.id).first()
        return obj


class InvestorUpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение инвестора"""

    serializer_class = InvestorUpdateSerializer
    http_method_names = [
        "get",
        "put",
    ]
    permission_classes = (IsAuthenticated, UpdatePermission)

    def get_object(self):
        obj = Investor.objects.filter(owner__id=self.request.user.id).first()
        return obj


class IndustriesListView(generics.ListAPIView):
    """Список всех индустрий"""

    queryset = Industries.objects.all()
    serializer_class = IndustriesSerializer


class BusinessTypeListView(generics.ListAPIView):
    """Список всех бизнес-типов"""

    queryset = BusinessType.objects.all()
    serializer_class = BusinessTypeSerializer


class RegionsListView(generics.ListAPIView):
    """Список всех регионов"""

    queryset = SaleRegions.objects.all()
    serializer_class = SaleRegionSerializer


# class ResumeListCreateView(generics.ListCreateAPIView):
#     """Список всех резюме профессионала | создание резюме"""
#
#     queryset = Resume.objects.all()
#     serializer_class = ResumeCreateSerializer
#     permission_classes = (IsAuthenticated, ProfessionalCreatePermission)
#
#     def get_queryset(self):
#         return Resume.objects.filter(professional_id__owner=self.request.user.id)
#
#
# class ResumeRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
#     """Получение | удаление | обновление резюме"""
#
#     queryset = Resume.objects.all()
#     serializer_class = ResumeUpdateSerializer
#     http_method_names = ["get", "put", "delete"]
#     permission_classes = [ResumePermission]


class AllStartupListView(generics.ListAPIView):
    """Список всех стартапов сайта"""

    queryset = Startup.objects.all()
    serializer_class = StartupSerializer


class AllStartupRetrieveView(generics.RetrieveAPIView):
    """Детальное получение стартапа"""

    queryset = Startup.objects.all()
    serializer_class = StartupSerializer


class AllProfessionalsListView(generics.ListAPIView):
    """Список всех профессионалов сайта"""

    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer


class AllProfessionalRetrieveView(generics.RetrieveAPIView):
    """Детальное получение профессионалов"""

    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer


class AllInvestorsListView(generics.ListAPIView):
    """Список всех инвесторов сайта"""

    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer


class AllInvestorsRetrieveView(generics.RetrieveAPIView):
    """Детальное получение инвестора"""

    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer
