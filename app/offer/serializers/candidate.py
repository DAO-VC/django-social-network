from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.utils import IntegrityError
from offer.models.offer import Offer
from offer.models.offer_candidate import CandidateStartup
from offer.serializers.offer import OfferBaseSerializer
from profiles.models.startup import Startup
from profiles.serializers.startup import StartupSerializer


class CandidateStartupBaseSerializer(serializers.ModelSerializer):
    """Базовый сериализатор кандидата на оффер"""

    # startup_id = serializers.PrimaryKeyRelatedField(read_only=True)
    startup_id = StartupSerializer(read_only=True)
    # offer_id = serializers.PrimaryKeyRelatedField(read_only=True)
    offer_id = OfferBaseSerializer(read_only=True)
    accept_status = serializers.CharField(read_only=True)

    class Meta:
        model = CandidateStartup
        fields = "__all__"


class CandidateStartupCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания кандидата на оффер"""

    startup_id = serializers.PrimaryKeyRelatedField(read_only=True)
    offer_id = serializers.PrimaryKeyRelatedField(read_only=True)
    accept_status = serializers.CharField(read_only=True)

    class Meta:
        model = CandidateStartup
        fields = "__all__"

    def create(self, validated_data):
        offer = get_object_or_404(Offer, pk=self.context.get("view").kwargs.get("pk"))
        startup = get_object_or_404(Startup, owner=self.context["request"].user)
        try:
            startup_candidate = CandidateStartup.objects.create(
                offer_id=offer,
                startup_id=startup,
                accept_status=CandidateStartup.AcceptStatus.PENDING_FOR_APPROVAL,
            )
        except IntegrityError:
            raise ValidationError("Вы уже подались на эту вакансию")

        return startup_candidate
