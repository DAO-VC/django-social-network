from django.urls import path

from profiles.views import StartUpCreateView

urlpatterns = [
    path("startup-onboarding/", StartUpCreateView.as_view(), name="create_startup"),
]
