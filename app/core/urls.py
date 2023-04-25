from django.urls import path

from core.views import (
    UserRegistrationView,
    UserLoginView,
    UserDestroyView,
    MeUserView,
    ResetPassword,
    ResetPasswordView,
    UserValidateEmailView,
)

urlpatterns = [
    path(
        "register/<str:profile_value>/", UserRegistrationView.as_view(), name="signup"
    ),
    path(
        "register/email/<int:pk>/", UserValidateEmailView.as_view(), name="verify_email"
    ),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserDestroyView.as_view(), name="logout"),
    path("me/", MeUserView.as_view(), name="me"),
    path("send-code/", ResetPassword.as_view(), name="request-password-reset"),
    path(
        "password-reset/<str:encoded_pk>/<str:token>/",
        ResetPasswordView.as_view(),
        name="reset_password",
    ),
]
