from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from vacancy.models.vacancy import Vacancy
from vacancy.permissions import VacancyGetCreatePermission, VacancyOwnerPermission
from vacancy.serializers.vacancy import (
    VacancyCreateSerializer,
    VacancyUpdateSerializer,
    VacancyVisibleSerializer,
    VacancyBaseSerializer,
)


class VacancyListCreateView(generics.ListCreateAPIView):
    """Список всех вакансий стартапа | создание вакансии"""

    serializer_class = VacancyCreateSerializer
    permission_classes = (IsAuthenticated, VacancyGetCreatePermission)

    def get_queryset(self):
        return Vacancy.objects.filter(
            Q(
                company_id__work_team__candidate_id__professional_id__owner__in=[
                    self.request.user.id
                ]
            )
            | Q(company_id__owner=self.request.user.id)
        )


class VacancyRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение | удаление вакансии"""

    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer
    http_method_names = ["get", "put", "delete"]
    permission_classes = (IsAuthenticated, VacancyOwnerPermission)


class VacancyVisibleRetrieveView(generics.UpdateAPIView):
    """Изменение видимости вакансии"""

    queryset = Vacancy.objects.all()
    serializer_class = VacancyVisibleSerializer
    http_method_names = ["put"]
    permission_classes = (IsAuthenticated, VacancyOwnerPermission)


class VacancyAllView(generics.ListAPIView):
    """Список всех вакансий | поиск по ним"""

    serializer_class = VacancyBaseSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["id", "company_id", "salary", "requirements"]
    ordering_fields = ["company_id", "position", "salary", "requirements", "created_at"]

    def get_queryset(self):
        return Vacancy.objects.filter(is_visible=True)


class VacancyAllDetailView(generics.RetrieveAPIView):
    """Все вакансии по id"""

    queryset = Vacancy.objects.all()
    serializer_class = VacancyBaseSerializer
    http_method_names = ["get"]


class StartupAllVacancies(generics.ListAPIView):
    """Список всех вакансий стартапа по id"""

    serializer_class = VacancyBaseSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Vacancy.objects.filter(company_id=self.kwargs["pk"])
