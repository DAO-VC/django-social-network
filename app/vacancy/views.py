from rest_framework import generics
from vacancy.models import Vacancy
from vacancy.serializers import VacancyCreateSerializer, VacancyUpdateSerializer


class VacancyListCreateView(generics.ListCreateAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyCreateSerializer

    def get_queryset(self):
        return Vacancy.objects.filter(company_id__owner_id=self.request.user.id)


class VacancyRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacancy.objects.all()
    serializer_class = VacancyUpdateSerializer
    http_method_names = ["put", "delete"]
