import django_filters
from django.db.models import Count, Sum

from vacancy.models.vacancy import Vacancy


class VacancyModelFilter(django_filters.FilterSet):
    skills = django_filters.CharFilter(method="skills_by_title")

    class Meta:
        model = Vacancy
        fields = ["skills", "salary_type", "work_schedule", "place"]

    # def skills_by_title(self, queryset, name, value):
    #     titles = value.split(",")  # Разбиваем список значений по запятой
    #
    #     queryset = queryset.annotate(count=Count("skills")).filter(count=len(titles))
    #
    #     for title in titles:
    #         queryset = queryset.filter(skills__title=title)
    #     return queryset

    def skills_by_title(self, queryset, name, value):
        titles = value.split(",")  # Разбиваем список значений по запятой

        return queryset.filter(skills__title__in=titles).distinct()
