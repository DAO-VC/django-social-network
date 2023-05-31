from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from offer.models import Offer
from profiles.models import Investor


class OfferBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор оффера"""

    investor_id = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Offer
        fields = "__all__"


class OfferCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания офера"""

    investor_id = serializers.SlugRelatedField(read_only=True, slug_field="id")

    class Meta:
        model = Offer
        fields = "__all__"

    def create(self, validated_data):
        investor: Investor = Investor.objects.filter(
            owner=self.context["request"].user
        ).first()

        industries = validated_data.pop("industries")
        if len(industries) < 1:
            raise ValidationError("Минимум одина индустрия")
        with transaction.atomic():
            offer = Offer.objects.create(**validated_data, investor_id=investor)
            offer.industries.set(industries)

        return offer


class OfferUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор обновления офера"""

    class Meta:
        model = Offer
        exclude = ("investor_id",)

    def update(self, instance, validated_data):
        industries = validated_data.pop("industries")
        if len(industries) > 0:
            instance.industries.set(industries)
        return super().update(instance, validated_data)


class OfferVisibleSerializer(serializers.ModelSerializer):
    """Сериализатор изменения видимости оффера"""

    class Meta:
        model = Offer
        fields = "__all__"
        read_only_fields = (
            "investor_id",
            "amount",
            "industries",
            "is_visible",
            "details",
            "created_at",
        )

    def update(self, instance: Offer, validated_data):
        if instance.is_visible:
            instance.is_visible = False
        else:
            instance.is_visible = True
        instance.save()
        return instance
