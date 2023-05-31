from django.urls import path

from offer.views import OfferListCreateView, OfferRetrieveUpdateDeleteView

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
]
