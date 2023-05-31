from django.urls import path

from offer.views import (
    OfferListCreateView,
    OfferRetrieveUpdateDeleteView,
    AllOffersList,
    AllOffersRetrieve,
    OfferVisibleRetrieveView,
)

urlpatterns = [
    path(
        "main/offers/",
        OfferListCreateView.as_view(),
        name="list_create_offer",
    ),
    path(
        "main/offers/<int:pk>/",
        OfferRetrieveUpdateDeleteView.as_view(),
        name="retrieve_offer",
    ),
    path(
        "main/offers/<int:pk>/visible/",
        OfferVisibleRetrieveView.as_view(),
        name="visible_retrieve_offer",
    ),
    path("common/offers/", AllOffersList.as_view(), name="all_offers"),
    path(
        "common/offers/<int:pk>/",
        AllOffersRetrieve.as_view(),
        name="all_detail_offers",
    ),
]
