from django_filters import rest_framework

from vacancy.models import Vacancy, Candidate


class VacancyFilter(rest_framework.FilterSet):
    class Meta:
        model = Vacancy
        fields = {
            "position": ("exact",),
        }


class CandidatesFilter(rest_framework.FilterSet):
    class Meta:
        model = Candidate
        fields = {
            "accept_status": ("exact",),
        }
