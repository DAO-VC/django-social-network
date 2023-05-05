from django.urls import path

from profiles.views import (
    StartUpCreateView,
    ProfessionalCreateView,
    InvestorCreateView,
    StartUpUpdateDetailView,
    ProfessionalUpdateDetailView,
    InvestorUpdateDetailView,
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
        "main/profiles/candidate/",
        ProfessionalUpdateDetailView.as_view(),
        name="update_delete_professional",
    ),
    path(
        "main/profiles/investor/",
        InvestorUpdateDetailView.as_view(),
        name="update_delete_investor",
    ),
]
