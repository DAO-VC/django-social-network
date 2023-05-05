from django.urls import path

from vacancy.views import VacancyListCreateView, VacancyRetrieveView

urlpatterns = [
    path(
        "main/vacancies/", VacancyListCreateView.as_view(), name="list_create_vacancy"
    ),
    path(
        "main/vacancies/<int:pk>",
        VacancyRetrieveView.as_view(),
        name="retrieve_vacancy",
    ),
]
