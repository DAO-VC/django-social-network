from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.utils import send_verification_mail

USER_MODEL = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
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
            raise serializers.ValidationError("Пароли не одинаковые")
        return data

    def create(self, validated_data):
        validated_data.pop("password_repeat")
        profile = self.context.get("view").kwargs.get("profile_value")
        user = USER_MODEL.objects.create_user(**validated_data)
        match profile:
            case "startup":
                user.profile = "startup"
        match profile:
            case "investor":
                user.profile = "investor"
        match profile:
            case "professional":
                user.profile = "professional"
        code = send_verification_mail(email=validated_data.get("email"))
        user.code = code
        user.save()
        return user


class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = "__all__"


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER_MODEL
        fields = ("email", "password")


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ("email",)


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, max_length=4)

    class Meta:
        fields = ("password",)

    def validate(self, data):
        password = data.get("password")
        token = self.context.get("kwargs").get("token")
        encoded_pk = self.context.get("kwargs").get("encoded_pk")

        if token is None or encoded_pk is None:
            raise ValidationError("Missing data")

        pk = urlsafe_base64_decode(encoded_pk).decode()
        user = USER_MODEL.objects.get(pk=pk)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise ValidationError("The reset token is invalid")

        USER_MODEL.set_password(password)
        USER_MODEL.save()
        return data


class UserCodeInputSerializer(serializers.ModelSerializer):
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
    def update(self, instance, validated_data):
        code = send_verification_mail(email=instance.email)
        instance.code = code
        instance.save()
        return instance

    class Meta:
        model = USER_MODEL
        fields = ()
