from django.urls import path

from profiles.views.investor import (
    InvestorCreateView,
    InvestorUpdateDetailView,
    AllInvestorsListView,
    AllInvestorsRetrieveView,
)
from profiles.views.other_views import (
    IndustriesListView,
    RegionsListView,
    BusinessTypeListView,
)
from profiles.views.professional import (
    ProfessionalCreateView,
    ProfessionalUpdateDetailView,
    AllProfessionalsListView,
    AllProfessionalRetrieveView,
)
from profiles.views.startup import (
    StartUpCreateView,
    StartUpUpdateDetailView,
    AllStartupListView,
    AllStartupRetrieveView,
)

urlpatterns = [
    path(
        "common/startup-onboarding/", StartUpCreateView.as_view(), name="create_startup"
    ),
    path(
        "common/investor-onboarding/",
        InvestorCreateView.as_view(),
        name="create_investor",
    ),
    path(
        "common/professional-onboarding/",
        ProfessionalCreateView.as_view(),
        name="create_professional",
    ),
    # path("main/companies/", StartListCreateView.as_view(), name="list_create_company"),
    path(
        "main/profiles/startup/",
        StartUpUpdateDetailView.as_view(),
        name="update_delete_company",
    ),
    path(
        "main/profiles/professional/",
        ProfessionalUpdateDetailView.as_view(),
        name="update_delete_professional",
    ),
    path(
        "main/profiles/investor/",
        InvestorUpdateDetailView.as_view(),
        name="update_delete_investor",
    ),
    path(
        "common/industries/",
        IndustriesListView.as_view(),
        name="industries_list",
    ),
    path(
        "common/regions/",
        RegionsListView.as_view(),
        name="regions_list",
    ),
    path(
        "common/business_types/",
        BusinessTypeListView.as_view(),
        name="business_type_list",
    ),
    path(
        "common/startups/",
        AllStartupListView.as_view(),
        name="all_startup_list",
    ),
    path(
        "common/startups/<int:pk>/",
        AllStartupRetrieveView.as_view(),
        name="all_startup_detail",
    ),
    path(
        "common/professionals/",
        AllProfessionalsListView.as_view(),
        name="all_professionals_list",
    ),
    path(
        "common/professionals/<int:pk>/",
        AllProfessionalRetrieveView.as_view(),
        name="all_professionals_detail",
    ),
    path(
        "common/investors/",
        AllInvestorsListView.as_view(),
        name="all_investors_list",
    ),
    path(
        "common/investors/<int:pk>/",
        AllInvestorsRetrieveView.as_view(),
        name="all_investors_detail",
    ),
]
