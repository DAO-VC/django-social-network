from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import transaction
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
import django.contrib.auth.password_validation as validators
from core.utils import send_verification_mail
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from vacancy.serializers.workteam import WorkTeamBaseSerializer

USER_MODEL = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Сариализатор регистрации пользователя"""

    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = USER_MODEL
        fields = (
            "id",
            "email",
            "password",
            "password_repeat",
            "first_name",
            "last_name",
            "phone",
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, data):
        validate_password(data)
        return data

    def validate_password_repeat(self, data):
        if data != self.initial_data.get("password"):
            raise serializers.ValidationError("Passwords are not the same")
        return data

    def create(self, validated_data):
        validated_data.pop("password_repeat")
        profile = self.context.get("view").kwargs.get("profile_value")
        email = validated_data.pop("email").lower()
        if USER_MODEL.objects.filter(email=email).exists():
            raise serializers.ValidationError("Not unique email")
        with transaction.atomic():
            user = USER_MODEL.objects.create_user(email=email, **validated_data)
            match profile:
                case "startup":
                    user.profile = "startup"
            match profile:
                case "investor":
                    user.profile = "investor"
            match profile:
                case "professional":
                    user.profile = "professional"

            code = send_verification_mail(email=email)
            # except Exception:
            #     user.delete()
            #     raise ParseError("Sorry ,please try again")
            user.code = code
            user.save()
        return user


class UserBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор пользователя"""

    permissions = WorkTeamBaseSerializer(read_only=True)

    class Meta:
        model = USER_MODEL
        fields = "__all__"


class UserLoginSerializer(serializers.ModelSerializer):
    """Сериализатор логина пользователя"""

    class Meta:
        model = USER_MODEL
        fields = ("email", "password")


class EmailSerializer(serializers.Serializer):
    """Email сериализатор"""

    email = serializers.EmailField()

    class Meta:
        fields = ("email",)


class ResetPasswordSerializer(serializers.Serializer):
    """Сериализатор восстановления пароля"""

    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        fields = ("password",)

    def validate(self, data):
        password = data.get("password")
        password_repeat = data.get("password_repeat")
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")

        if token is None or encoded_pk is None:
            raise ValidationError("Missing data")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = USER_MODEL.objects.get(pk=pk)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise ValidationError("The reset token is invalid")
        if password != password_repeat:
            raise ValidationError("Password mismatch!")
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)
        except ValidationError as e:
            raise ValidationError(e)
        user.set_password(password)
        user.is_active = True
        user.save()
        return data


class UserCodeInputSerializer(serializers.ModelSerializer):
    """Сериализатор ввода проверочного кода"""

    code = serializers.CharField(write_only=True, max_length=7)

    def update(self, instance, validated_data):
        code = validated_data.get("code")
        if not instance.code == code:
            raise ValidationError("Verification code is not valid")

        instance.is_active = True
        instance.save()
        return instance

    class Meta:
        model = USER_MODEL
        fields = ("code",)


class UserCodeUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор отправки нового  проверочного кода"""

    def update(self, instance, validated_data):
        with transaction.atomic():
            code = send_verification_mail(email=instance.email)
            instance.code = code
            instance.save()
        return instance

    class Meta:
        model = USER_MODEL
        fields = ()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Надстройка над JWT login"""

    def validate(self, attrs):
        attrs["email"] = attrs.get("email").lower()
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data
