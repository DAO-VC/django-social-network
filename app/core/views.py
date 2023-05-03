import json

from django.contrib.auth import authenticate, login, get_user_model, logout, get_user
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    GenericAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.urls import reverse
from rest_framework.views import APIView
from django.utils.encoding import force_bytes
from core.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserBaseSerializer,
    ResetPasswordSerializer,
    EmailSerializer,
    UserCodeInputSerializer,
    UserCodeUpdateSerializer,
)
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode

from core.utils import send_emails

User = get_user_model()


class UserRegistrationView(CreateAPIView):
    """Регистрация нового пользователя"""

    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


# @method_decorator(csrf_exempt, name="dispatch")
@method_decorator(ensure_csrf_cookie)
class UserLoginView(APIView):
    """Логин пользователя"""

    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request):
        data = json.loads(request.body)
        email = data.get("email")
        if email in [None, ""]:
            return JsonResponse(
                {"email": ["Введите email"]}, status=status.HTTP_400_BAD_REQUEST
            )
        password = data.get("password")
        if password in [None, ""]:
            return JsonResponse(
                {"password": ["Введите пароль"]}, status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return JsonResponse(UserLoginSerializer(User).data)
        return JsonResponse(
            {"error": "Invalid login"}, status=status.HTTP_404_NOT_FOUND
        )


class UserDestroyView(DestroyAPIView):
    """Логаут пользователя"""

    queryset = User.objects.all()
    serializer_class = UserBaseSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = get_user(self.request)
        return obj

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=204)


class MeUserView(ListAPIView):
    """Эндпоинт /me для получения данных текущего пользователя"""

    queryset = User.objects.all()
    serializer_class = UserBaseSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        self.queryset = User.objects.filter(id=self.request.user.pk)
        return self.queryset


class ResetPassword(GenericAPIView):
    """Генерация и отправка токена для сброса пароля"""

    serializer_class = EmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_url = reverse(
                "reset_password",
                kwargs={"encoded_pk": encoded_pk, "token": token},
            )
            reset_link = f"localhost:8000{reset_url}"
            try:
                send_emails(recipient_email=email, message_url=reset_link)
                return Response("Success. Check Your Email")
            except Exception as e:
                print(e)
                # TODO : добавить логгер
                return Response("Something wrong")

        else:
            return Response(
                {"message": "User don't exist"}, status=status.HTTP_400_BAD_REQUEST
            )


class ResetPasswordView(GenericAPIView):
    """Генерация нового пароля после перехода по url"""

    serializer_class = ResetPasswordSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"kwargs": kwargs}
        )
        serializer.is_valid(raise_exception=True)

        return Response(
            {"message": "Password reset complete"}, status=status.HTTP_200_OK
        )


class UserValidateEmailView(UpdateAPIView):
    """PUT - Верификация | PATCH - Отправка нового кода Email"""

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.method == "PUT":
            return UserCodeInputSerializer

        if self.request.method == "PATCH":
            return UserCodeUpdateSerializer

    def get_object(self):
        obj = get_object_or_404(User, id=self.kwargs.get("pk"))
        return obj


class MeUserDeleteView(DestroyAPIView):
    """Эндпоинт  для удаления данных  пользователя"""

    queryset = User.objects.all()
    serializer_class = UserBaseSerializer
