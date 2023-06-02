from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from offer.models.offer import Offer, ConfirmedOffer
from offer.models.offer_candidate import CandidateStartup
from profiles.models.investor import Investor
from profiles.serializers.investor import InvestorSerializer
from profiles.serializers.startup import StartupSerializer


class OfferBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор оффера"""

    # investor_id = serializers.SlugRelatedField(read_only=True, slug_field="id")
    investor_id = InvestorSerializer(read_only=True)

    class Meta:
        model = Offer
        fields = "__all__"


class OfferCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания офера"""

    investor_id = serializers.SlugRelatedField(read_only=True, slug_field="id")
    is_visible = serializers.BooleanField(read_only=True)

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
            offer = Offer.objects.create(
                **validated_data, investor_id=investor, is_visible=True
            )
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


class ConfirmOfferSerializer(serializers.ModelSerializer):
    """Сериализатор подтверждения кандидата на оффер"""

    class Meta:
        model = CandidateStartup
        fields = "__all__"
        read_only_fields = (
            "startup_id",
            "offer_id",
            "accept_status",
            "created_at",
        )

    def update(self, instance: CandidateStartup, validated_data):
        instance.accept_status = CandidateStartup.AcceptStatus.ACCEPT
        instance.save()
        new_confirmed_offer = ConfirmedOffer(
            startup_id=instance.startup_id, investor_id=instance.offer_id.investor_id
        )
        new_confirmed_offer.save()
        return super().update(instance, validated_data)


class ConfirmedOfferInvestorSerializer(serializers.ModelSerializer):
    startup_id = StartupSerializer(read_only=True)

    class Meta:
        model = ConfirmedOffer
        fields = "__all__"


class ConfirmedOfferStartupSerializer(serializers.ModelSerializer):
    investor_id = InvestorSerializer(read_only=True)

    class Meta:
        model = ConfirmedOffer
        fields = "__all__"
