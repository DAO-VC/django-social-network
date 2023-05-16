from django_filters import rest_framework

from vacancy.models import Vacancy


class VacancyFilter(rest_framework.FilterSet):
    class Meta:
        model = Vacancy
        fields = {
            "company_id": ("exact",),
        }
