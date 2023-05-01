from django.urls import path

from profiles.views import StartUpCreateView, ProfessionalCreateView, InvestorCreateView

urlpatterns = [
    path("startup-onboarding/", StartUpCreateView.as_view(), name="create_startup"),
    path("investor-onboarding/", InvestorCreateView.as_view(), name="create_investor"),
    path(
        "professional-onboarding/",
        ProfessionalCreateView.as_view(),
        name="create_professional",
    ),
]
