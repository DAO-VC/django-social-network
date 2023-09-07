from django.urls import path

from offer.views.candidate import (
    ListAllOfferCandidates,
    ConfirmOfferView,
    InvestorConfirmedStartupsList,
    StartupConfirmedRetrieveDeleteView,
    StartupCandidateCreateView,
    StartupConfirmedList,
    StartupMyApplications,
    OfferFavoriteCandidates,
    InvestCandidateFavoriteRetrieveView,
    OfferRetrieveStartupCandidates,
    StartupMyApplicationsRetrieveView,
)
from offer.views.offer import (
    OfferListCreateView,
    OfferRetrieveUpdateDeleteView,
    OfferVisibleRetrieveView,
    AllOffersList,
    AllOffersRetrieve,
    InvestorAllOffers,
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
    # path(
    #     "main/offers/candidates/",
    #     OfferStartupCandidates.as_view(),
    #     name="all_startups_candidates_to_investor",
    # ),
    path(
        "main/offers/candidates/<int:pk>/",
        OfferRetrieveStartupCandidates.as_view(),
        name="retrieve_delete_startup_candidate_to_offer",
    ),
    path(
        "main/offers/<int:pk>/candidates/",
        ListAllOfferCandidates.as_view(),
        name="all_startups_candidates_to_offer",
    ),
    path(
        "main/offers/<int:pk>/confirm/",
        ConfirmOfferView.as_view(),
        name="confirm_investing_to_startup",
    ),
    path(
        "main/confirmed_offers/",
        InvestorConfirmedStartupsList.as_view(),
        name="all_confirmed_offers",
    ),
    path(
        "main/confirmed_offers/<int:pk>/",
        StartupConfirmedRetrieveDeleteView.as_view(),
        name="retrieve_delete_confirmed_offer",
    ),
    path("common/offers/", AllOffersList.as_view(), name="all_offers"),
    path(
        "common/offers/<int:pk>/",
        AllOffersRetrieve.as_view(),
        name="all_detail_offers",
    ),
    path(
        "common/investor/<int:pk>/offers/",
        InvestorAllOffers.as_view(),
        name="all_offers_to_investor",
    ),
    path(
        "common/offers/<int:pk>/apply/",
        StartupCandidateCreateView.as_view(),
        name="apply_startup_to_offer",
    ),
    path(
        "main/startup/investments/",
        StartupConfirmedList.as_view(),
        name="all_startup_investors_list",
    ),
    path(
        "main/startup/applications/",
        StartupMyApplications.as_view(),
        name="all_startup_applications_list",
    ),
    path(
        "main/startup/applications/<int:pk>/",
        StartupMyApplicationsRetrieveView.as_view(),
        name="retrieve_applications_startup",
    ),
    path(
        "main/investor/favorites/",
        OfferFavoriteCandidates.as_view(),
        name="all_favorites_to_investor",
    ),
    path(
        "main/investor/candidates/<int:pk>/favorite/",
        InvestCandidateFavoriteRetrieveView.as_view(),
        name="add/remove_offer_candidate_to_favorite",
    ),
]
