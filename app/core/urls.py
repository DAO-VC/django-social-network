from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from core.views import (
    UserRegistrationView,
    MeUserView,
    ResetPassword,
    ResetPasswordView,
    UserValidateEmailView,
    MeUserDeleteView,
)

urlpatterns = [
    path(
        "register/<str:profile_value>/", UserRegistrationView.as_view(), name="signup"
    ),
    path(
        "register/email/<int:pk>/", UserValidateEmailView.as_view(), name="verify_email"
    ),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", MeUserView.as_view(), name="me"),
    path("user/<int:pk>", MeUserDeleteView.as_view(), name="delete_user"),
    path("send-code/", ResetPassword.as_view(), name="request-password-reset"),
    path(
        "password-reset/<str:encoded_pk>/<str:token>/",
        ResetPasswordView.as_view(),
        name="reset_password",
    ),
]
