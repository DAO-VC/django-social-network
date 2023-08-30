from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from offer.models.offer import Offer, ConfirmedOffer
from offer.models.offer_candidate import CandidateStartup
from profiles.models.investor import Investor
from profiles.serializers.investor import InvestorSerializer
from profiles.serializers.startup import StartupSerializer
from vacancy.models.vacancy import Skill
from django.db.utils import IntegrityError


class OfferBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор оффера"""

    # investor_id = serializers.SlugRelatedField(read_only=True, slug_field="id")
    total_candidates = serializers.SerializerMethodField(read_only=True)
    investor_id = InvestorSerializer(read_only=True)
    industries = serializers.SlugRelatedField(
        many=True, slug_field="title", read_only=True
    )

    class Meta:
        model = Offer
        fields = "__all__"

    def get_total_candidates(self, instance: Offer):
        return instance.offer_to_candidate.filter(
            accept_status=CandidateStartup.AcceptStatus.PENDING_FOR_APPROVAL,
        ).count()


class OfferCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания офера"""

    investor_id = serializers.SlugRelatedField(read_only=True, slug_field="id")
    industries = serializers.SlugRelatedField(
        many=True, slug_field="title", read_only=True
    )
    update_industries = serializers.ListField(
        child=serializers.CharField(max_length=50), write_only=True
    )
    active_status = serializers.CharField(read_only=True)

    class Meta:
        model = Offer
        fields = "__all__"

    def create(self, validated_data):
        investor: Investor = Investor.objects.filter(
            owner=self.context["request"].user
        ).first()

        industries_titles = validated_data.pop("update_industries")
        with transaction.atomic():
            offer = Offer.objects.create(
                **validated_data,
                investor_id=investor,
                active_status=Offer.ActiveStatus.ACTIVE,
            )
            update_industries = []
            for title in industries_titles:
                industries, created = Skill.objects.get_or_create(title=title)
                update_industries.append(industries)
        offer.industries.set(update_industries)
        return offer


class OfferUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор обновления офера"""

    industries = serializers.SlugRelatedField(
        many=True, slug_field="title", read_only=True
    )
    update_industries = serializers.ListField(
        child=serializers.CharField(max_length=54), write_only=True
    )
    active_status = serializers.CharField(read_only=True)

    class Meta:
        model = Offer
        exclude = ("investor_id",)

    def update(self, instance: Offer, validated_data):
        industries_titles = validated_data.pop("update_industries")
        with transaction.atomic():
            new_industries = []
            for title in industries_titles:
                industries, created = Skill.objects.get_or_create(title=title)
                new_industries.append(industries)
        instance.industries.set(new_industries)
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
            "offer_information",
            "created_at",
            "caption",
            "active_status",
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
            "about",
            "is_favorite",
            "active_status",
        )

    def update(self, instance: CandidateStartup, validated_data):
        instance.accept_status = CandidateStartup.AcceptStatus.ACCEPT
        instance.save()
        try:
            ConfirmedOffer.objects.create(
                startup_id=instance.startup_id,
                investor_id=instance.offer_id.investor_id,
                offer_id=instance.offer_id,
            )
        except IntegrityError:
            raise ValidationError(
                f"This startup already in confirmed offers  Investor {instance.offer_id.investor_id}"
            )

        return super().update(instance, validated_data)


class ConfirmedOfferInvestorSerializer(serializers.ModelSerializer):
    startup_id = StartupSerializer(read_only=True)
    offer_id = OfferBaseSerializer(read_only=True)

    class Meta:
        model = ConfirmedOffer
        fields = "__all__"


class ConfirmedOfferStartupSerializer(serializers.ModelSerializer):
    investor_id = InvestorSerializer(read_only=True)
    offer_id = OfferBaseSerializer(read_only=True)

    class Meta:
        model = ConfirmedOffer
        fields = "__all__"
