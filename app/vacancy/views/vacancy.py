from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated

from vacancy.filters import VacancyModelFilter
from vacancy.models.vacancy import Vacancy
from vacancy.permissions import (
    VacancyGetCreatePermission,
    VacancyOwnerPermission,
    RetrieveVacancyPermission,
)
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
    filterset_fields = ["id", "active_status"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return VacancyCreateSerializer
        return VacancyBaseSerializer

    def get_queryset(self):
        return (
            Vacancy.objects.select_related(
                "company_id",
            )
            .prefetch_related("skills", "requirements")
            .filter(
                Q(
                    company_id__work_team__candidate_id__professional_id__owner__in=[
                        self.request.user.id
                    ]
                )
                | Q(company_id__owner=self.request.user.id)
            )
        ).distinct()


class VacancyRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    """Изменение | удаление вакансии"""

    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer
    http_method_names = ["get", "put", "delete"]
    permission_classes = (RetrieveVacancyPermission,)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return VacancyBaseSerializer
        return VacancyUpdateSerializer

    def perform_destroy(self, instance: Vacancy):
        instance.active_status = Vacancy.ActiveStatus.ARCHIVE
        instance.save()
        return instance


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
    filterset_class = VacancyModelFilter
    ordering_fields = ["company_id", "position", "salary", "requirements", "created_at"]
    search_fields = ("salary", "salary_type", "description", "company_id", "position")

    def get_queryset(self):
        return (
            Vacancy.objects.select_related(
                "company_id",
            )
            .prefetch_related("skills", "requirements")
            .filter(is_visible=True)
        )


class StartupAllVacancies(generics.ListAPIView):
    """Список всех вакансий стартапа по id"""

    serializer_class = VacancyBaseSerializer

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return (
            Vacancy.objects.select_related(
                "company_id",
            )
            .prefetch_related("skills", "requirements")
            .filter(company_id=self.kwargs["pk"])
        )
