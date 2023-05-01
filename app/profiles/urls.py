from django.urls import path

from profiles.views import StartUpCreateView, ProfessionalCreateView

urlpatterns = [
    path("startup-onboarding/", StartUpCreateView.as_view(), name="create_startup"),
    path(
        "professional-onboarding/",
        ProfessionalCreateView.as_view(),
        name="create_professional",
    ),
]
