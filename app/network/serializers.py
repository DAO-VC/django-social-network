from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from network.models import Network
from django.db import transaction
from django.db.utils import IntegrityError
from image.tasks import cleaner


class CreateMyNetworkSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Network
        fields = "__all__"

    def create(self, validated_data):
        current_user = self.context.get("request").user

        interests = validated_data.pop("interests")
        if len(interests) < 1:
            raise ValidationError("Min one interest")
        try:
            with transaction.atomic():
                network = Network.objects.create(
                    **validated_data, owner=current_user, is_active=True
                )
                network.interests.set(interests)
        except IntegrityError:
            transaction.rollback()
            raise ValidationError("Network for this user is already exist")
        return network


class NetworkBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = "__all__"


class UpdateNetworkSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Network
        fields = "__all__"

    def update(self, instance: Network, validated_data):
        interests = validated_data.pop("interests")
        if len(interests) < 1:
            raise ValidationError("Min one interest")
        instance.interests.set(interests)

        if instance.logo:
            object_logo_id = instance.logo.id
            new_logo_id = validated_data.get("logo")
            if new_logo_id:
                new_logo_id = new_logo_id.id

            cleaner.delay(object_logo_id, new_logo_id)

        return super().update(instance, validated_data)


class MyNetworkChangeStatusSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)

    def update(self, instance: Network, validated_data):
        instance.change_active()
        return super().update(instance, validated_data)

    class Meta:
        model = Network
        exclude = ("owner", "logo", "interests", "about")
