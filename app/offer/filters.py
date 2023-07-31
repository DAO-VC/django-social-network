import django_filters
from django.db.models import Count, Sum

from offer.models.offer import Offer


class OfferModelFilter(django_filters.FilterSet):
    industries = django_filters.CharFilter(method="industries_by_title")
    salary = django_filters.CharFilter(method="salary_filter")

    class Meta:
        model = Offer
        fields = ["industries", "salary"]

    # def industries_by_title(self, queryset, name, value):
    #     titles = value.split(",")  # Разбиваем список значений по запятой
    #
    #     queryset = queryset.annotate(count=Count("industries")).filter(
    #         count=len(titles)
    #     )
    #
    #     for title in titles:
    #         queryset = queryset.filter(industries__title=title)
    #     return queryset
    def industries_by_title(self, queryset, name, value):
        titles = value.split(",")  # Разбиваем список значений по запятой

        return queryset.filter(industries__title__in=titles).distinct()

    def salary_filter(self, queryset, name, value):
        match value:
            case "less_then_1000":
                return queryset.filter(amount__lt=1000)

            case "1000–3000":
                return queryset.filter(amount__lte=3000, amount__gte=1001)

            case "3001-5000":
                return queryset.filter(amount__lte=5000, amount__gte=3001)

            case "5001-7000":
                return queryset.filter(amount__lte=7000, amount__gte=5001)

            case "more_then_7000":
                return queryset.filter(amount__gte=7001)

            case _:
                return queryset
