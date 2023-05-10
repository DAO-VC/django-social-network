from django.urls import path

from vacancy.views import (
    VacancyListCreateView,
    VacancyRetrieveView,
    OfferListCreateView,
    OfferRetrieveUpdateDeleteView,
)

urlpatterns = [
    path(
        "main/vacancies/", VacancyListCreateView.as_view(), name="list_create_vacancy"
    ),
    path(
        "main/vacancies/<int:pk>",
        VacancyRetrieveView.as_view(),
        name="retrieve_vacancy",
    ),
    path(
        "main/offers/",
        OfferListCreateView.as_view(),
        name="list_create_offer",
    ),
    path(
        "main/offers/<int:pk>",
        OfferRetrieveUpdateDeleteView.as_view(),
        name="retrieve_offer",
    ),
]
